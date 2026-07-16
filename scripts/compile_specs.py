#!/usr/bin/env python3
"""Deterministic spec-compiler for Phase 2 feature specs.

Every specs/features/FEAT-##.spec.md has two kinds of body zones:

  * ``<!-- COMPILER:BEGIN x -->...<!-- COMPILER:END x -->`` - owned by THIS
    script. Regenerated VERBATIM from the member REQs (traceability, acceptance
    scenarios, NFR table, dependency graph, provenance). Never hand-edit.
  * ``<!-- FILL:x -->...<!-- /FILL -->`` - authored by the Copilot cloud agent
    (intent, scope, grounding, open-decisions). Never touched here.

``spec_hash`` in the front-matter is the SHA-256 over the compiler zones. It lets
a downstream stage trust that the compiler zones still match their REQ source.

Modes:
  (default)  rewrite the compiler zones + spec_hash in place (idempotent).
  --check    do NOT write; exit 1 if regenerating would change any file
             (i.e. the specs have drifted from the reviewed REQ set). Used by CI.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print(f"::error::missing dependency: {exc}. Run: pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
FEAT_DIR = ROOT / "specs" / "features"
REQ_DIR = ROOT / "specs" / "requirements"

ZONE_ORDER = ["traceability", "scenarios", "nfr", "deps", "provenance"]

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
GHERKIN_BODY = re.compile(r"```gherkin\b\n(.*?)\n```", re.DOTALL)
NFR_SECTION = re.compile(r"(?ms)^## NFR\b.*?(?=^## |\Z)")
YAML_BLOCK = re.compile(r"```yaml\b\n(.*?)\n```", re.DOTALL)


def parse_body_nfr(body: str) -> list[dict]:
    """Extract the structured NFR list from a REQ body '## NFR' yaml block."""
    sec = NFR_SECTION.search(body)
    if not sec:
        return []
    block = YAML_BLOCK.search(sec.group(0))
    if not block:
        return []
    try:
        data = yaml.safe_load(block.group(1)) or {}
    except yaml.YAMLError:
        return []
    items = data.get("nfr") if isinstance(data, dict) else None
    return [i for i in (items or []) if isinstance(i, dict)]


def _zone_re(name: str) -> re.Pattern:
    return re.compile(
        rf"(<!-- COMPILER:BEGIN {re.escape(name)} -->\n)(.*?)(\n<!-- COMPILER:END {re.escape(name)} -->)",
        re.DOTALL,
    )


def split_front_matter(text: str):
    m = FRONT_MATTER.match(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def read_req(req_id: str):
    """Return (front_matter_dict, body) for a member REQ, or None if missing."""
    path = REQ_DIR / f"{req_id}.md"
    if not path.exists():
        return None
    fm_raw, body = split_front_matter(path.read_text(encoding="utf-8"))
    if fm_raw is None:
        return None
    fm = yaml.safe_load(fm_raw) or {}
    return fm, (body or "")


def _cell(value) -> str:
    return "—" if value in (None, "", []) else str(value)


def build_zone(name: str, reqs: list[tuple[dict, str]]) -> str:
    """Deterministically render one compiler zone from the member REQs."""
    if name == "traceability":
        rows = ["| REQ | Title | Type | Priority | Status |", "|-----|-------|------|----------|--------|"]
        for fm, _ in reqs:
            rows.append(
                f"| {_cell(fm.get('id'))} | {_cell(fm.get('title'))} | "
                f"{_cell(fm.get('type'))} | {_cell(fm.get('priority'))} | {_cell(fm.get('status'))} |"
            )
        return "\n".join(rows)

    if name == "scenarios":
        blocks = []
        for _, body in reqs:
            m = GHERKIN_BODY.search(body)
            if m:
                blocks.append(m.group(1).strip())
        return "```gherkin\n" + "\n\n".join(blocks) + "\n```"

    if name == "nfr":
        rows = ["| Metric | Target | Source REQ |", "|--------|--------|------------|"]
        any_nfr = False
        for fm, body in reqs:
            for entry in parse_body_nfr(body):
                any_nfr = True
                rows.append(f"| {_cell(entry.get('metric'))} | {_cell(entry.get('target'))} | {_cell(fm.get('id'))} |")
        if not any_nfr:
            rows.append("| (none) | — | — |")
        return "\n".join(rows)

    if name == "deps":
        lines = []
        for fm, _ in reqs:
            deps = fm.get("depends_on") or []
            if deps:
                lines.append(f"{fm.get('id')} → {', '.join(deps)}")
        return "\n".join(lines) if lines else "(none)"

    if name == "provenance":
        rows = ["| REQ | Source File | SHA-256 | Location |", "|-----|-------------|---------|----------|"]
        for fm, _ in reqs:
            rows.append(
                f"| {_cell(fm.get('id'))} | {_cell(fm.get('source_file'))} | "
                f"{_cell(fm.get('sha256'))} | {_cell(fm.get('location'))} |"
            )
        return "\n".join(rows)

    raise ValueError(f"unknown zone: {name}")


def hash_compiler_zones(text: str) -> str:
    """SHA-256 over the (stripped, ordered) compiler-zone contents of a spec."""
    parts = []
    for name in ZONE_ORDER:
        m = _zone_re(name).search(text)
        parts.append((m.group(2).strip() if m else ""))
    joined = "\n".join(parts).replace("\r\n", "\n")
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def recompile(text: str, reqs: list[tuple[dict, str]]) -> str:
    """Return the spec text with all compiler zones + spec_hash regenerated."""
    for name in ZONE_ORDER:
        zone = build_zone(name, reqs)
        pat = _zone_re(name)
        if pat.search(text):
            text = pat.sub(lambda mo: mo.group(1) + zone + mo.group(3), text)
    new_hash = hash_compiler_zones(text)
    text = re.sub(r'(?m)^spec_hash:\s*.*$', f'spec_hash: "{new_hash}"', text, count=1)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="fail (exit 1) if any spec would change; do not write")
    args = ap.parse_args()

    specs = sorted(FEAT_DIR.glob("FEAT-*.spec.md"))
    if not specs:
        print("::warning::no FEAT specs found under specs/features/")
        return 0

    drifted: list[str] = []
    errors: list[str] = []

    for spec in specs:
        rel = spec.relative_to(ROOT).as_posix()
        text = spec.read_text(encoding="utf-8")
        fm_raw, _ = split_front_matter(text)
        if fm_raw is None:
            errors.append(f"::error file={rel}::missing YAML front-matter")
            continue
        fm = yaml.safe_load(fm_raw) or {}
        member_reqs = fm.get("member_reqs") or []

        reqs = []
        missing = False
        for rid in member_reqs:
            r = read_req(rid)
            if r is None:
                errors.append(f"::error file={rel}::member REQ not found or malformed: {rid}")
                missing = True
            else:
                reqs.append(r)
        if missing:
            continue

        new_text = recompile(text, reqs)
        if new_text != text:
            if args.check:
                drifted.append(rel)
            else:
                spec.write_text(new_text, encoding="utf-8", newline="\n")
                print(f"compiled: {rel}")

    for e in errors:
        print(e)

    if errors:
        print(f"\nCompile FAILED: {len(errors)} error(s).")
        return 1

    if args.check:
        if drifted:
            for rel in drifted:
                print(f"::error file={rel}::compiler zones or spec_hash are stale - run: python scripts/compile_specs.py")
            print(f"\nCompile check FAILED: {len(drifted)} spec(s) drifted from the REQ source.")
            return 1
        print(f"Compile check passed: {len(specs)} spec(s) in sync with the REQ source.")
        return 0

    print(f"\nCompiled {len(specs)} spec(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

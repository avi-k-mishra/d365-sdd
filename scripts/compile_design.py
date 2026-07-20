#!/usr/bin/env python3
"""Deterministic design-compiler for Phase 3 design & UX specs.

Every specs/design/DES-##.md and specs/ux/UX-##.md has two kinds of body zones:

  * ``<!-- COMPILER:BEGIN x -->...<!-- COMPILER:END x -->`` - owned by THIS
    script. Regenerated VERBATIM from the source feature/design spec and its
    member REQs (traceability chain FEAT<-REQ<-INTK, NFR carry-over, provenance).
    Never hand-edit.
  * ``<!-- FILL:x -->...<!-- /FILL -->`` - authored by the Copilot cloud agent
    grounded via Microsoft Learn MCP (the 8 decision axes + rationale, solution,
    observability, surfaces, ...). Never touched here.

``spec_hash`` in the front-matter is the SHA-256 over the compiler zones. It lets
a downstream stage trust that the compiler zones still match their source.

This mirrors scripts/compile_specs.py (Stage 2). The deterministic/LLM split is
the crux: anything derivable from the approved feature spec is compiler-owned;
only architectural judgment is agent-owned.

Modes:
  (default)  rewrite the compiler zones + spec_hash in place (idempotent).
  --check    do NOT write; exit 1 if regenerating would change any file
             (i.e. a design has drifted from its approved feature source). CI.
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
DESIGN_DIR = ROOT / "specs" / "design"
UX_DIR = ROOT / "specs" / "ux"
FEAT_DIR = ROOT / "specs" / "features"
REQ_DIR = ROOT / "specs" / "requirements"

DES_ZONES = ["traceability", "nfr", "provenance"]
UX_ZONES = ["traceability", "provenance"]

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
NFR_SECTION = re.compile(r"(?ms)^## NFR\b.*?(?=^## |\Z)")
YAML_BLOCK = re.compile(r"```yaml\b\n(.*?)\n```", re.DOTALL)


def split_front_matter(text: str):
    m = FRONT_MATTER.match(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def _read(path: Path):
    """Return (front_matter_dict, body) for a spec file, or None if missing/bad."""
    if not path.exists():
        return None
    fm_raw, body = split_front_matter(path.read_text(encoding="utf-8"))
    if fm_raw is None:
        return None
    try:
        fm = yaml.safe_load(fm_raw) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    return fm, (body or "")


def read_req(req_id: str):
    return _read(REQ_DIR / f"{req_id}.md")


def read_feat(feat_id: str):
    return _read(FEAT_DIR / f"{feat_id}.spec.md")


def read_des(des_id: str):
    return _read(DESIGN_DIR / f"{des_id}.md")


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


def _cell(value) -> str:
    return "—" if value in (None, "", []) else str(value)


def build_zone(name: str, kind: str, ctx: dict) -> str:
    """Deterministically render one compiler zone from the source spec + REQs.

    ctx carries: reqs (list of (fm, body)), source_id (FEAT or DES id),
    self_id (DES or UX id), feature_id.
    """
    reqs = ctx["reqs"]

    if name == "traceability":
        anchor = "Feature" if kind == "DES" else "Design"
        anchor_id = ctx["source_id"]
        rows = [
            f"| REQ | Title | Intake Batch | {anchor} |",
            "|-----|-------|--------------|--------|",
        ]
        for fm, _ in reqs:
            rows.append(
                f"| {_cell(fm.get('id'))} | {_cell(fm.get('title'))} | "
                f"{_cell(fm.get('intake_batch'))} | {_cell(anchor_id)} |"
            )
        return "\n".join(rows)

    if name == "nfr":
        rows = ["| Metric | Target | Source REQ |", "|--------|--------|------------|"]
        any_nfr = False
        for fm, body in reqs:
            for entry in parse_body_nfr(body):
                any_nfr = True
                rows.append(
                    f"| {_cell(entry.get('metric'))} | {_cell(entry.get('target'))} | {_cell(fm.get('id'))} |"
                )
        if not any_nfr:
            rows.append("| (none) | — | — |")
        return "\n".join(rows)

    if name == "provenance":
        req_ids = ", ".join(_cell(fm.get("id")) for fm, _ in reqs) or "—"
        if kind == "DES":
            rows = [
                "| Design | Feature | Member REQs |",
                "|--------|---------|-------------|",
                f"| {_cell(ctx['self_id'])} | {_cell(ctx['source_id'])} | {req_ids} |",
            ]
        else:  # UX
            rows = [
                "| Experience | Design | Feature | REQs |",
                "|------------|--------|---------|------|",
                f"| {_cell(ctx['self_id'])} | {_cell(ctx['source_id'])} | "
                f"{_cell(ctx.get('feature_id'))} | {req_ids} |",
            ]
        return "\n".join(rows)

    raise ValueError(f"unknown zone: {name}")


def hash_compiler_zones(text: str, zones: list[str]) -> str:
    """SHA-256 over the (stripped, ordered) compiler-zone contents of a spec."""
    parts = []
    for name in zones:
        m = _zone_re(name).search(text)
        parts.append((m.group(2).strip() if m else ""))
    joined = "\n".join(parts).replace("\r\n", "\n")
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def resolve_context(kind: str, fm: dict):
    """Return (ctx, errors). ctx has the member REQs and lineage ids."""
    errors: list[str] = []
    self_id = fm.get("id")

    if kind == "DES":
        source_id = fm.get("implements_feature")
        feat = read_feat(source_id) if isinstance(source_id, str) else None
        if feat is None:
            errors.append(f"implements_feature not found or malformed: {source_id}")
            return None, errors
        ffm, _ = feat
        member_ids = ffm.get("member_reqs") or []
        feature_id = source_id
    else:  # UX
        source_id = fm.get("implements_design")
        des = read_des(source_id) if isinstance(source_id, str) else None
        if des is None:
            errors.append(f"implements_design not found or malformed: {source_id}")
            return None, errors
        dfm, _ = des
        member_ids = dfm.get("satisfies") or []
        feature_id = dfm.get("implements_feature")

    reqs = []
    for rid in member_ids:
        r = read_req(rid)
        if r is None:
            errors.append(f"member REQ not found or malformed: {rid}")
        else:
            reqs.append(r)
    if errors:
        return None, errors

    ctx = {
        "reqs": reqs,
        "source_id": source_id,
        "self_id": self_id,
        "feature_id": feature_id,
    }
    return ctx, errors


def recompile(text: str, kind: str, ctx: dict) -> str:
    """Return the spec text with all compiler zones + spec_hash regenerated."""
    zones = DES_ZONES if kind == "DES" else UX_ZONES
    for name in zones:
        pat = _zone_re(name)
        if pat.search(text):
            zone = build_zone(name, kind, ctx)
            text = pat.sub(lambda mo: mo.group(1) + zone + mo.group(3), text)
    new_hash = hash_compiler_zones(text, zones)
    text = re.sub(r'(?m)^spec_hash:\s*.*$', f'spec_hash: "{new_hash}"', text, count=1)
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="fail (exit 1) if any spec would change; do not write")
    args = ap.parse_args()

    targets = [("DES", p) for p in sorted(DESIGN_DIR.glob("DES-*.md"))]
    targets += [("UX", p) for p in sorted(UX_DIR.glob("UX-*.md"))]
    if not targets:
        print("::warning::no DES/UX specs found under specs/design/ or specs/ux/")
        return 0

    drifted: list[str] = []
    errors: list[str] = []

    for kind, spec in targets:
        rel = spec.relative_to(ROOT).as_posix()
        text = spec.read_text(encoding="utf-8")
        fm_raw, _ = split_front_matter(text)
        if fm_raw is None:
            errors.append(f"::error file={rel}::missing YAML front-matter")
            continue
        try:
            fm = yaml.safe_load(fm_raw) or {}
        except yaml.YAMLError as e:
            errors.append(f"::error file={rel}::invalid YAML front-matter: {e}")
            continue

        ctx, ctx_errors = resolve_context(kind, fm)
        if ctx is None:
            for e in ctx_errors:
                errors.append(f"::error file={rel}::{e}")
            continue

        new_text = recompile(text, kind, ctx)
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
                print(f"::error file={rel}::compiler zones or spec_hash are stale - run: python scripts/compile_design.py")
            print(f"\nCompile check FAILED: {len(drifted)} spec(s) drifted from the approved source.")
            return 1
        print(f"Compile check passed: {len(targets)} spec(s) in sync with the approved source.")
        return 0

    print(f"\nCompiled {len(targets)} spec(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

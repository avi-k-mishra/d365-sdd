#!/usr/bin/env python3
"""Deterministic validator (T1) for atomic requirement files.

Validates every specs/requirements/REQ-####.md against:
  1. specs/_schema/req.schema.json           (front-matter shape)
  2. provenance: source_file must exist under intake/
  3. id sequencing: REQ ids are sequential, zero-padded, no gaps/dups
  4. body sections: a testable statement + '## Acceptance scenarios'
     containing a ```gherkin block

Hard failures exit 1 and print ::error:: annotations (block the PR).
Soft issues (e.g. confidence: low) print ::warning:: and do NOT fail.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print(f"::error::missing dependency: {exc}. Run: pip install pyyaml jsonschema")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
REQ_DIR = ROOT / "specs" / "requirements"
SCHEMA_PATH = ROOT / "specs" / "_schema" / "req.schema.json"

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
GHERKIN_BLOCK = re.compile(r"```gherkin\b.*?```", re.DOTALL)

errors: list[str] = []
warnings: list[str] = []


def err(file: str, msg: str) -> None:
    errors.append(f"::error file={file}::{msg}")


def warn(file: str, msg: str) -> None:
    warnings.append(f"::warning file={file}::{msg}")


def split_front_matter(text: str):
    m = FRONT_MATTER.match(text)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"::error::schema not found: {SCHEMA_PATH}")
        return 2
    validator = Draft202012Validator(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))

    files = sorted(REQ_DIR.glob("REQ-*.md"))
    if not files:
        print("::warning::no REQ files found under specs/requirements/")
        return 0

    seen_ids: dict[int, str] = {}

    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text(encoding="utf-8")

        fm_raw, body = split_front_matter(text)
        if fm_raw is None:
            err(rel, "missing YAML front-matter delimited by '---' lines")
            continue

        try:
            fm = yaml.safe_load(fm_raw) or {}
        except yaml.YAMLError as e:
            err(rel, f"invalid YAML front-matter: {e}")
            continue
        if not isinstance(fm, dict):
            err(rel, "front-matter must be a YAML mapping")
            continue

        # 1. schema
        for v in sorted(validator.iter_errors(fm), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in v.path) or "(root)"
            err(rel, f"schema: {loc}: {v.message}")

        # filename must match the id
        fid = fm.get("id")
        if isinstance(fid, str) and f.stem != fid:
            err(rel, f"filename '{f.stem}' does not match id '{fid}'")

        # 2. provenance: source file exists under intake/
        src = fm.get("source_file")
        if isinstance(src, str) and src.startswith("intake/"):
            if not (ROOT / src).exists():
                err(rel, f"source_file does not exist on disk: {src}")

        # id sequencing bookkeeping
        if isinstance(fid, str):
            m = re.match(r"^REQ-([0-9]{4})$", fid)
            if m:
                n = int(m.group(1))
                if n in seen_ids:
                    err(rel, f"duplicate id {fid} (also in {seen_ids[n]})")
                else:
                    seen_ids[n] = rel

        # 3. body sections
        body = body or ""
        statement = re.sub(r"^#.*$", "", body, flags=re.MULTILINE).strip()
        if len(statement) < 15:
            err(rel, "requirement statement is empty or too short")
        if "## Acceptance scenarios" not in body:
            err(rel, "missing '## Acceptance scenarios' section")
        elif not GHERKIN_BLOCK.search(body):
            err(rel, "'## Acceptance scenarios' has no ```gherkin block")

        # soft: low confidence and security-without-negative
        if fm.get("confidence") == "low":
            warn(rel, "confidence: low - flagged for human review")
        if fm.get("type") == "security":
            gher = "\n".join(GHERKIN_BLOCK.findall(body)).lower()
            if "negative" not in gher:
                err(rel, "security REQ must include a 'negative' acceptance scenario")

    # 3b. no gaps in the id sequence
    if seen_ids:
        nums = sorted(seen_ids)
        expected = list(range(1, nums[-1] + 1))
        missing = sorted(set(expected) - set(nums))
        if missing:
            gaps = ", ".join(f"REQ-{n:04d}" for n in missing)
            errors.append(f"::error::gap in REQ id sequence - missing: {gaps}")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    total = len(files)
    if errors:
        print(f"\nREQ validation FAILED: {len(errors)} error(s) across {total} file(s).")
        return 1
    print(f"\nREQ validation passed: {total} file(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

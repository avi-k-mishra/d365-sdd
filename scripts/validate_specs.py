#!/usr/bin/env python3
"""Deterministic validator (T1) for Phase 2 feature specs.

Validates every specs/features/FEAT-##.spec.md against:
  1. specs/_schema/feature.schema.json         (front-matter shape)
  2. filename matches id; FEAT ids are sequential, zero-padded, no gaps/dups
  3. membership: every member REQ exists, and each member REQ front-matter
     points back with feature: <this FEAT> and epic: <this EPIC>
  3d. intake_batches equals the union of the members' intake_batch
  4. coverage: every REQ that declares feature: FEAT-XX is listed in that
     feature's member_reqs (no orphaned or mis-filed requirements)
  5. body zones: all COMPILER + FILL zones present; FILL zones are authored
     (non-empty, no leftover placeholder); the scenarios zone has a gherkin block
  6. integrity: spec_hash matches the SHA-256 of the current compiler zones
     (i.e. scripts/compile_specs.py has been run and nothing was hand-edited)

Hard failures exit 1 and print ::error:: annotations (block the PR).
Soft issues print ::warning:: and do NOT fail.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compile_specs as C  # shared zone/hash logic - single source of truth

ROOT = Path(__file__).resolve().parents[1]
FEAT_DIR = ROOT / "specs" / "features"
REQ_DIR = ROOT / "specs" / "requirements"
SCHEMA_PATH = ROOT / "specs" / "_schema" / "feature.schema.json"

FILL_ZONES = ["intent", "scope", "grounding", "open-decisions"]
FILL_RE = {z: re.compile(rf"<!-- FILL:{re.escape(z)} -->\n(.*?)\n<!-- /FILL -->", re.DOTALL) for z in FILL_ZONES}

errors: list[str] = []
warnings: list[str] = []


def err(file: str, msg: str) -> None:
    errors.append(f"::error file={file}::{msg}")


def warn(file: str, msg: str) -> None:
    warnings.append(f"::warning file={file}::{msg}")


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"::error::schema not found: {SCHEMA_PATH}")
        return 2
    validator = Draft202012Validator(json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))

    specs = sorted(FEAT_DIR.glob("FEAT-*.spec.md"))
    if not specs:
        print("::warning::no FEAT specs found under specs/features/")
        return 0

    seen_ids: dict[int, str] = {}
    req_to_feature: dict[str, str] = {}  # member REQ -> owning FEAT (from specs)

    for spec in specs:
        rel = spec.relative_to(ROOT).as_posix()
        text = spec.read_text(encoding="utf-8")

        fm_raw, body = C.split_front_matter(text)
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

        # 2. filename + id sequencing
        fid = fm.get("id")
        if isinstance(fid, str) and spec.name != f"{fid}.spec.md":
            err(rel, f"filename does not match id '{fid}' (expected {fid}.spec.md)")
        if isinstance(fid, str):
            m = re.match(r"^FEAT-([0-9]{2})$", fid)
            if m:
                n = int(m.group(1))
                if n in seen_ids:
                    err(rel, f"duplicate id {fid} (also in {seen_ids[n]})")
                else:
                    seen_ids[n] = rel

        # 3. membership: each member REQ exists and points back
        epic = fm.get("epic")
        member_batches: set[str] = set()
        for rid in fm.get("member_reqs") or []:
            r = C.read_req(rid)
            if r is None:
                err(rel, f"member REQ not found or malformed: {rid}")
                continue
            rfm, _ = r
            if rfm.get("feature") != fid:
                err(rel, f"{rid} front-matter feature is '{rfm.get('feature')}', expected '{fid}'")
            if rfm.get("epic") != epic:
                err(rel, f"{rid} front-matter epic is '{rfm.get('epic')}', expected '{epic}'")
            mb = rfm.get("intake_batch")
            if isinstance(mb, str):
                member_batches.add(mb)
            if rid in req_to_feature:
                err(rel, f"{rid} is also a member of {req_to_feature[rid]}")
            else:
                req_to_feature[rid] = fid

        # 3d. intake_batches must equal the union of the members' intake_batch
        declared_batches = set(fm.get("intake_batches") or [])
        if declared_batches != member_batches:
            err(
                rel,
                f"intake_batches {sorted(declared_batches)} does not match the union of "
                f"member REQ intake_batch {sorted(member_batches)}",
            )

        # 5. body zones
        body = body or ""
        for name in C.ZONE_ORDER:
            if not C._zone_re(name).search(body):
                err(rel, f"missing COMPILER zone '{name}'")
        for name, pat in FILL_RE.items():
            fm_match = pat.search(body)
            if not fm_match:
                err(rel, f"missing FILL zone '{name}'")
            elif len(fm_match.group(1).strip()) < 3:
                err(rel, f"FILL zone '{name}' is empty - agent authoring required")
        sc = C._zone_re("scenarios").search(body)
        if sc and "```gherkin" not in sc.group(2):
            err(rel, "scenarios COMPILER zone has no ```gherkin block")

        # 6. integrity: spec_hash matches the compiler zones
        declared = fm.get("spec_hash")
        actual = C.hash_compiler_zones(body)
        if isinstance(declared, str) and declared != actual:
            err(rel, "spec_hash is stale - run: python scripts/compile_specs.py")

    # 3b. no gaps in the FEAT id sequence
    if seen_ids:
        nums = sorted(seen_ids)
        missing = sorted(set(range(1, nums[-1] + 1)) - set(nums))
        if missing:
            gaps = ", ".join(f"FEAT-{n:02d}" for n in missing)
            errors.append(f"::error::gap in FEAT id sequence - missing: {gaps}")

    # 4. coverage: every REQ that names a feature must be a listed member of it
    for req_file in sorted(REQ_DIR.glob("REQ-*.md")):
        rfm, _ = C.split_front_matter(req_file.read_text(encoding="utf-8"))
        if rfm is None:
            continue
        try:
            data = yaml.safe_load(rfm) or {}
        except yaml.YAMLError:
            continue
        feat = data.get("feature")
        rid = data.get("id")
        if isinstance(feat, str) and req_to_feature.get(rid) != feat:
            rel = req_file.relative_to(ROOT).as_posix()
            err(rel, f"{rid} declares feature '{feat}' but is not listed in its member_reqs")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    total = len(specs)
    if errors:
        print(f"\nFeature validation FAILED: {len(errors)} error(s) across {total} spec(s).")
        return 1
    print(f"\nFeature validation passed: {total} spec(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Deterministic validator (T1 - DesValidator) for Phase 3 design & UX specs.

Validates every specs/design/DES-##.md against:
  1. specs/_schema/design.schema.json          (front-matter shape)
  2. filename matches id; DES ids sequential, zero-padded, no gaps/dups
  3. traceability totality: implements_feature resolves to a real FEAT spec,
     satisfies equals that feature's member_reqs, and no two DES design the
     same feature (no orphan design / double-claimed feature)
  4. body zones: all COMPILER + FILL zones present; FILL zones authored
  5. all 10 decision axes present with a rationale for any escalation; every
     primary component bullet in the solution zone's `components:` list is tagged
     with a known component_type (conventions.yml component_types); and every such
     component declares its per-type required payload as `- <field>:` sub-lines
     (conventions.yml component_type_payloads; legacy + legacy_payload designs exempt)
  6. open_questions resolved (no unchecked '- [ ]' left in the open-questions zone)
  7. integrity: spec_hash matches the SHA-256 of the current compiler zones

and every specs/ux/UX-##.md against:
  1. specs/_schema/ux.schema.json
  2. filename/id sequencing (UX-##)
  3. implements_design resolves to a real DES; satisfies equals that DES's satisfies
  4. body zones present + authored; 6. open_questions resolved; 7. spec_hash intact

NFR carry-over integrity is covered by scripts/compile_design.py --check (the
compiler regenerates the carry-over table verbatim from the source REQs).

Hard failures exit 1 and print ::error:: annotations (block the PR).
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
import compile_design as C  # shared zone/hash logic - single source of truth

ROOT = Path(__file__).resolve().parents[1]
DESIGN_DIR = ROOT / "specs" / "design"
UX_DIR = ROOT / "specs" / "ux"
SCHEMA_DIR = ROOT / "specs" / "_schema"
CONVENTIONS = ROOT / "conventions.yml"

DES_FILL_ZONES = ["decisions", "solution", "observability", "open-questions"]
UX_FILL_ZONES = ["surfaces", "client-logic", "components", "navigation-accessibility", "open-questions"]

FALLBACK_AXES = [
    "logic_tier", "data_residency", "alm_boundary", "security",
    "integration", "environment", "ux_surface", "observability",
    "batch_processing", "reporting",
]
FALLBACK_BASELINE_AXES = [
    "logic_tier", "data_residency", "alm_boundary", "security",
    "integration", "environment", "ux_surface", "observability",
]
ESCALATION_RE = re.compile(r"\b(low_code|pro_code)\b", re.IGNORECASE)
UNRESOLVED_RE = re.compile(r"(?m)^\s*[-*]\s*\[\s\]")  # an unchecked markdown checkbox

errors: list[str] = []
warnings: list[str] = []


def err(file: str, msg: str) -> None:
    errors.append(f"::error file={file}::{msg}")


def fill_re(zone: str) -> re.Pattern:
    return re.compile(rf"<!-- FILL:{re.escape(zone)} -->\n(.*?)\n<!-- /FILL -->", re.DOTALL)


def load_decision_axes() -> list[str]:
    if CONVENTIONS.exists():
        try:
            data = yaml.safe_load(CONVENTIONS.read_text(encoding="utf-8")) or {}
            axes = data.get("decision_axes")
            if isinstance(axes, list) and axes:
                return [str(a) for a in axes]
        except yaml.YAMLError:
            pass
    return FALLBACK_AXES


def load_component_types() -> list[str]:
    # The closed component_type vocabulary. Entries ending in '_*' (e.g.
    # 'config_ai_*', 'mcs_*', 'code_webres_*') are parameterised prefixes.
    return _load_conventions_list("component_types", [])


COMPONENT_TYPE_RE = re.compile(r"component_type:\s*([A-Za-z0-9_]+)")
# A payload sub-line beneath a component bullet: `  - <field>: <value>`.
SUBKEY_RE = re.compile(r"^\s*-\s*([A-Za-z0-9_]+)\s*:")

# The `components:` sub-list inside a DES solution FILL zone: from the
# `- **components:**` header up to the next top-level `- **<key>:**` or the
# end of the zone. Only the bullets in this block are components to be tagged
# (other lists like test_strategy/security legitimately have untagged bullets).
COMPONENTS_BLOCK_RE = re.compile(
    r"(?im)^\s*-\s*\*\*components:\*\*.*?\n(.*?)(?=^\s*-\s*\*\*|\Z)", re.DOTALL
)
BULLET_RE = re.compile(r"^(\s*)-\s+\S")


def component_type_allowed(value: str, vocab: list[str]) -> bool:
    if value in vocab:
        return True
    for entry in vocab:
        if entry.endswith("_*") and value.startswith(entry[:-1]):
            return True
    return False


def _load_conventions_list(key: str, fallback: list[str]) -> list[str]:
    if CONVENTIONS.exists():
        try:
            data = yaml.safe_load(CONVENTIONS.read_text(encoding="utf-8")) or {}
            val = data.get(key)
            if isinstance(val, list) and val:
                return [str(a) for a in val]
        except yaml.YAMLError:
            pass
    return fallback


def load_baseline_axes() -> list[str]:
    # Minimum axes required of every design, including legacy ones authored
    # before later axes were added. New designs must satisfy the full set.
    return _load_conventions_list("decision_axes_baseline", FALLBACK_BASELINE_AXES)


def load_legacy_designs() -> list[str]:
    # DES ids exempt from axes added beyond the baseline until they are refreshed.
    return _load_conventions_list("legacy_designs", [])


def load_legacy_payload_designs() -> list[str]:
    # DES ids that predate the Design-item payload contract; exempt from per-type
    # required-payload enforcement until refreshed.
    return _load_conventions_list("legacy_payload_designs", [])


def load_component_payloads() -> dict:
    # Map: component_type -> {"required": [field, ...]}. Single source of truth for
    # the minimum fields each design item must declare (see the Design-item payload
    # contract in specs/_schema/component-types.md). Wildcard keys end in '_*'.
    if CONVENTIONS.exists():
        try:
            data = yaml.safe_load(CONVENTIONS.read_text(encoding="utf-8")) or {}
            val = data.get("component_type_payloads")
            if isinstance(val, dict) and val:
                return val
        except yaml.YAMLError:
            pass
    return {}


def required_fields_for(ctype: str, payloads: dict) -> list[str]:
    entry = payloads.get(ctype)
    if entry is None:
        for key, val in payloads.items():
            if key.endswith("_*") and ctype.startswith(key[:-1]):
                entry = val
                break
    if entry is None:
        entry = payloads.get("_default", {"required": ["name", "satisfies"]})
    req = entry.get("required") if isinstance(entry, dict) else None
    return [str(f) for f in (req or ["name", "satisfies"])]


def check_common_zones(rel, body, compiler_zones, fill_zones):
    for name in compiler_zones:
        if not C._zone_re(name).search(body):
            err(rel, f"missing COMPILER zone '{name}'")
    for name in fill_zones:
        m = fill_re(name).search(body)
        if not m:
            err(rel, f"missing FILL zone '{name}'")
        elif len(m.group(1).strip()) < 3:
            err(rel, f"FILL zone '{name}' is empty - agent authoring required")
    # open-questions must be resolved
    oq = fill_re("open-questions").search(body)
    if oq and UNRESOLVED_RE.search(oq.group(1)):
        err(rel, "unresolved open question ('- [ ]') remains - must be closed before Gate A/B")


def check_spec_hash(rel, fm, body, zones):
    declared = fm.get("spec_hash")
    actual = C.hash_compiler_zones(body, zones)
    if isinstance(declared, str) and declared != actual:
        err(rel, "spec_hash is stale - run: python scripts/compile_design.py")


def check_id_sequence(seen, prefix):
    if not seen:
        return
    nums = sorted(seen)
    missing = sorted(set(range(1, nums[-1] + 1)) - set(nums))
    if missing:
        gaps = ", ".join(f"{prefix}-{n:02d}" for n in missing)
        errors.append(f"::error::gap in {prefix} id sequence - missing: {gaps}")


def main() -> int:
    des_schema_path = SCHEMA_DIR / "design.schema.json"
    ux_schema_path = SCHEMA_DIR / "ux.schema.json"
    if not des_schema_path.exists() or not ux_schema_path.exists():
        print(f"::error::schema not found under {SCHEMA_DIR}")
        return 2
    des_validator = Draft202012Validator(json.loads(des_schema_path.read_text(encoding="utf-8")))
    ux_validator = Draft202012Validator(json.loads(ux_schema_path.read_text(encoding="utf-8")))
    axes = load_decision_axes()
    baseline_axes = load_baseline_axes()
    legacy_designs = set(load_legacy_designs())
    legacy_payload_designs = set(load_legacy_payload_designs())
    component_types = load_component_types()
    component_payloads = load_component_payloads()

    designs = sorted(DESIGN_DIR.glob("DES-*.md"))
    uxs = sorted(UX_DIR.glob("UX-*.md"))
    if not designs and not uxs:
        print("::warning::no DES/UX specs found under specs/design/ or specs/ux/")
        return 0

    des_seen: dict[int, str] = {}
    feature_to_des: dict[str, str] = {}
    des_satisfies: dict[str, list] = {}

    # ---- DES ----
    for spec in designs:
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
        body = body or ""

        for v in sorted(des_validator.iter_errors(fm), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in v.path) or "(root)"
            err(rel, f"schema: {loc}: {v.message}")

        did = fm.get("id")
        if isinstance(did, str):
            if spec.name != f"{did}.md":
                err(rel, f"filename does not match id '{did}' (expected {did}.md)")
            m = re.match(r"^DES-([0-9]{2})$", did)
            if m:
                n = int(m.group(1))
                if n in des_seen:
                    err(rel, f"duplicate id {did} (also in {des_seen[n]})")
                else:
                    des_seen[n] = rel
            des_satisfies[did] = fm.get("satisfies") or []

        # traceability totality
        feat_id = fm.get("implements_feature")
        feat = C.read_feat(feat_id) if isinstance(feat_id, str) else None
        if feat is None:
            err(rel, f"implements_feature not found or malformed: {feat_id}")
        else:
            ffm, _ = feat
            member = ffm.get("member_reqs") or []
            satisfies = fm.get("satisfies") or []
            if sorted(satisfies) != sorted(member):
                err(rel, f"satisfies {sorted(satisfies)} != feature {feat_id} member_reqs {sorted(member)}")
            if isinstance(feat_id, str):
                if feat_id in feature_to_des:
                    err(rel, f"feature {feat_id} is also designed by {feature_to_des[feat_id]}")
                else:
                    feature_to_des[feat_id] = did if isinstance(did, str) else rel

        check_common_zones(rel, body, C.DES_ZONES, DES_FILL_ZONES)

        # decision axes present, escalation rationale.
        # Legacy designs (listed in conventions.yml legacy_designs) only need the
        # baseline axes until they are refreshed; all other designs need the full set.
        dz = fill_re("decisions").search(body)
        if dz:
            dtext = dz.group(1)
            required_axes = baseline_axes if (isinstance(did, str) and did in legacy_designs) else axes
            for axis in required_axes:
                if axis not in dtext:
                    err(rel, f"decision axis '{axis}' missing from the decisions zone")
            if ESCALATION_RE.search(dtext) and "rationale" not in dtext.lower():
                err(rel, "logic-tier escalation (low_code/pro_code) without a recorded rationale")

        # component_type tagging: every component bullet in the DES solution
        # zone's `components:` list must carry a component_type from the closed
        # vocabulary (conventions.yml component_types). Legacy designs
        # (predating the taxonomy) are exempt.
        if not (isinstance(did, str) and did in legacy_designs) and component_types:
            sol = fill_re("solution").search(body)
            if sol:
                soltext = sol.group(1)
                for t in COMPONENT_TYPE_RE.findall(soltext):
                    if not component_type_allowed(t, component_types):
                        err(rel, f"unknown component_type '{t}' - not in conventions.yml component_types")
                cblock = COMPONENTS_BLOCK_RE.search(soltext)
                if not cblock or not cblock.group(1).strip():
                    err(rel, "solution zone has no 'components:' list - tag each component (see specs/_schema/component-types.md)")
                else:
                    # Enforce a component_type on every primary component bullet
                    # (the least-indented bullets under `components:`), so nested
                    # detail bullets are not falsely flagged.
                    bullets = [(m.group(1), ln) for ln in cblock.group(1).splitlines()
                               for m in [BULLET_RE.match(ln)] if m]
                    if bullets:
                        min_indent = min(len(indent) for indent, _ in bullets)
                        tagged = 0
                        for indent, ln in bullets:
                            if len(indent) == min_indent:
                                if "component_type:" in ln:
                                    tagged += 1
                                else:
                                    err(rel, f"component without a component_type tag: {ln.strip()[:70]} (see specs/_schema/component-types.md)")
                        if tagged == 0:
                            err(rel, "components list has no 'component_type:' tags - tag each component (see specs/_schema/component-types.md)")

                        # Per-type required payload: every primary component must
                        # declare its conventions.yml component_type_payloads fields
                        # as indented `- <field>:` sub-lines (name comes from the
                        # bullet header). Designs predating the payload contract
                        # (conventions.yml legacy_payload_designs) are exempt.
                        payload_exempt = isinstance(did, str) and (
                            did in legacy_designs or did in legacy_payload_designs
                        )
                        if not payload_exempt and component_payloads:
                            comps: list[dict] = []
                            current: dict | None = None
                            for indent, ln in bullets:
                                if len(indent) == min_indent:
                                    tm = COMPONENT_TYPE_RE.search(ln)
                                    current = {"ctype": tm.group(1) if tm else None,
                                               "line": ln, "keys": set()}
                                    comps.append(current)
                                elif current is not None and len(indent) > min_indent:
                                    km = SUBKEY_RE.match(ln)
                                    if km:
                                        current["keys"].add(km.group(1))
                            for comp in comps:
                                if not comp["ctype"]:
                                    continue
                                for field in required_fields_for(comp["ctype"], component_payloads):
                                    if field == "name":
                                        continue
                                    if field not in comp["keys"]:
                                        err(rel, f"component '{comp['line'].strip()[:50]}' ({comp['ctype']}) missing required payload field '{field}' (see the Design-item payload contract in specs/_schema/component-types.md)")

        check_spec_hash(rel, fm, body, C.DES_ZONES)

    check_id_sequence(des_seen, "DES")

    # ---- UX ----
    ux_seen: dict[int, str] = {}
    for spec in uxs:
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
        body = body or ""

        for v in sorted(ux_validator.iter_errors(fm), key=lambda e: list(e.path)):
            loc = "/".join(str(p) for p in v.path) or "(root)"
            err(rel, f"schema: {loc}: {v.message}")

        uid = fm.get("id")
        if isinstance(uid, str):
            if spec.name != f"{uid}.md":
                err(rel, f"filename does not match id '{uid}' (expected {uid}.md)")
            m = re.match(r"^UX-([0-9]{2})$", uid)
            if m:
                n = int(m.group(1))
                if n in ux_seen:
                    err(rel, f"duplicate id {uid} (also in {ux_seen[n]})")
                else:
                    ux_seen[n] = rel

        des_id = fm.get("implements_design")
        if not isinstance(des_id, str) or des_id not in des_satisfies:
            err(rel, f"implements_design not found among DES specs: {des_id}")
        else:
            satisfies = fm.get("satisfies") or []
            if sorted(satisfies) != sorted(des_satisfies[des_id]):
                err(rel, f"satisfies {sorted(satisfies)} != design {des_id} satisfies {sorted(des_satisfies[des_id])}")

        check_common_zones(rel, body, C.UX_ZONES, UX_FILL_ZONES)
        check_spec_hash(rel, fm, body, C.UX_ZONES)

    check_id_sequence(ux_seen, "UX")

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    total = len(designs) + len(uxs)
    if errors:
        print(f"\nDesign validation FAILED: {len(errors)} error(s) across {total} spec(s).")
        return 1
    print(f"\nDesign validation passed: {total} spec(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

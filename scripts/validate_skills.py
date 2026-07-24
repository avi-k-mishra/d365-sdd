#!/usr/bin/env python3
"""Deterministic validator (T1) for the component_type skill library.

Verifies that the three sources of truth stay mutually consistent:
  1. conventions.yml `component_type_skills` (skill -> covered component_types)
  2. conventions.yml `component_types` (the closed vocabulary) and
     `component_type_payloads` (per-type required fields)
  3. the authored skill files under .github/skills/<skill>/

Checks:
  A. Map integrity — every component_type in the vocabulary is covered by exactly
     one skill; every type in the map exists in the vocabulary (no orphan/invented
     types, no duplicates across skills).
  B. Payload homes — every `component_type_payloads` key (except `_default`) is a
     real component_type in the vocabulary.
  C. Authored skills — for every skill whose folder already exists under
     .github/skills/, require a SKILL.md carrying `name`/`description`
     front-matter and one `<component_type>.md` reference per covered type. A
     wildcard type `x_*` maps to the reference file `x.md`.
  D. No orphans — every `<skill>/*.md` (other than SKILL.md) corresponds to a
     covered component_type of that skill.

Skills that are mapped but not yet authored (no folder) are reported as
informational skips (deferred), not failures — Phase-B skills and any Phase-A
skill not yet replicated from the dataverse-table template. Hard failures exit 1
and print ::error:: annotations (block the PR).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print(f"::error::missing dependency: {exc}. Run: pip install pyyaml")
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CONVENTIONS = ROOT / "conventions.yml"
SKILLS_DIR = ROOT / ".github" / "skills"

FRONT_MATTER = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

errors: list[str] = []
notes: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"::error file={where}::{msg}")


def ref_filename(ctype: str) -> str:
    # A wildcard type `x_*` is served by the reference file `x.md`.
    base = ctype[:-2] if ctype.endswith("_*") else ctype
    return f"{base}.md"


def matches_type(value: str, vocab: set[str]) -> bool:
    if value in vocab:
        return True
    for entry in vocab:
        if entry.endswith("_*") and value.startswith(entry[:-1]):
            return True
    return False


def main() -> int:
    if not CONVENTIONS.exists():
        print(f"::error::conventions.yml not found at {CONVENTIONS}")
        return 2
    data = yaml.safe_load(CONVENTIONS.read_text(encoding="utf-8")) or {}

    skills = data.get("component_type_skills") or {}
    vocab_list = data.get("component_types") or []
    payloads = data.get("component_type_payloads") or {}
    phases = data.get("skill_phases") or {}

    if not isinstance(skills, dict) or not skills:
        print("::error::conventions.yml component_type_skills is missing or empty")
        return 1

    vocab = {str(t) for t in vocab_list}
    phase_of = {}
    for ph, names in phases.items():
        for s in (names or []):
            phase_of[str(s)] = str(ph)

    rel_conv = CONVENTIONS.relative_to(ROOT).as_posix()

    # ---- A. Map integrity ----
    seen: dict[str, str] = {}
    for skill, types in skills.items():
        if not isinstance(types, list) or not types:
            err(rel_conv, f"skill '{skill}' maps to no component_types")
            continue
        for t in types:
            t = str(t)
            if t in seen:
                err(rel_conv, f"component_type '{t}' mapped to multiple skills ('{seen[t]}' and '{skill}')")
            else:
                seen[t] = skill
            if t not in vocab:
                err(rel_conv, f"skill '{skill}' covers '{t}', which is not in conventions.yml component_types")
    for t in sorted(vocab):
        if t not in seen:
            err(rel_conv, f"component_type '{t}' is not covered by any skill in component_type_skills")

    # ---- B. Payload homes ----
    for t in payloads:
        if t == "_default":
            continue
        if not matches_type(str(t), vocab):
            err(rel_conv, f"component_type_payloads has an entry for '{t}', which is not a known component_type")

    # ---- C/D. Authored skills ----
    for skill, types in skills.items():
        if not isinstance(types, list):
            continue
        folder = SKILLS_DIR / skill
        expected = {ref_filename(str(t)) for t in types}

        if not folder.exists():
            ph = phase_of.get(skill, "?")
            notes.append(f"::notice::skill '{skill}' (Phase {ph}) not authored yet - skipped (deferred)")
            continue

        rel_skill = f".github/skills/{skill}"
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            err(rel_skill, f"skill '{skill}' is missing SKILL.md")
        else:
            fm = FRONT_MATTER.search(skill_md.read_text(encoding="utf-8"))
            if not fm:
                err(f"{rel_skill}/SKILL.md", "SKILL.md is missing YAML front-matter (--- name/description ---)")
            else:
                try:
                    meta = yaml.safe_load(fm.group(1)) or {}
                except yaml.YAMLError as e:
                    meta = {}
                    err(f"{rel_skill}/SKILL.md", f"invalid front-matter YAML: {e}")
                for key in ("name", "description"):
                    if not meta.get(key):
                        err(f"{rel_skill}/SKILL.md", f"SKILL.md front-matter missing required '{key}'")
                if meta.get("name") and str(meta["name"]) != skill:
                    err(f"{rel_skill}/SKILL.md", f"SKILL.md name '{meta['name']}' does not match folder '{skill}'")

        # one reference file per covered type
        present = {p.name for p in folder.glob("*.md") if p.name != "SKILL.md"}
        for t in types:
            fname = ref_filename(str(t))
            if fname not in present:
                err(rel_skill, f"skill '{skill}' is missing reference file '{fname}' for component_type '{t}'")
        # orphan reference files
        for name in sorted(present - expected):
            err(f"{rel_skill}/{name}", f"orphan reference file '{name}' - no matching covered component_type in skill '{skill}'")

    for n in notes:
        print(n)
    for e in errors:
        print(e)

    if errors:
        print(f"\nSkill-library validation FAILED: {len(errors)} error(s).")
        return 1
    print(f"\nSkill-library validation passed: {len(skills)} skill(s), {len(vocab)} component_type(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

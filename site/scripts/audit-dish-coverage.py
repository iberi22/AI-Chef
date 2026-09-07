#!/usr/bin/env python3
"""
Audit dish frontmatter coverage across site/src/content/dishes/**/*.md.
Excludes README.md and collection index files (recetas_*.md).
Stdlib only.
"""

import glob
import os
import re
import sys


def parse_frontmatter(content):
    """
    Parses frontmatter block from markdown content into a dict of fields.
    Stdlib regex-based YAML parser for dish frontmatter schema.
    """
    if not content.startswith("---"):
        return {}, content

    # Ensure --- is followed by newline or content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm_text = parts[1]
    body = parts[2]

    data = {}
    current_key = None
    current_subdict = None

    lines = fm_text.splitlines()
    for line in lines:
        raw_line = line
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        top_match = re.match(r"^([a-zA-Z0-9_]+):\s*(.*)$", line)
        indent_match = re.match(r"^\s+([a-zA-Z0-9_]+):\s*(.*)$", raw_line)
        list_match = re.match(r"^\s*-\s+(.*)$", raw_line)

        if list_match and current_key:
            item_val = list_match.group(1).strip().strip("'\"")
            if current_subdict and current_key in data and isinstance(data[current_key], dict):
                sub_key = current_subdict
                if sub_key in data[current_key] and isinstance(data[current_key][sub_key], list):
                    data[current_key][sub_key].append(item_val)
                else:
                    data[current_key][sub_key] = [item_val]
            else:
                if current_key in data and isinstance(data[current_key], list):
                    data[current_key].append(item_val)
                else:
                    data[current_key] = [item_val]
            continue

        if indent_match and current_key and isinstance(data.get(current_key), dict):
            sub_k = indent_match.group(1)
            sub_v = indent_match.group(2).strip()
            current_subdict = sub_k
            if sub_v:
                sub_v_clean = sub_v.strip("'\"")
                data[current_key][sub_k] = sub_v_clean
            else:
                data[current_key][sub_k] = []
            continue

        if top_match:
            k = top_match.group(1)
            v = top_match.group(2).strip()
            current_key = k
            current_subdict = None

            if not v:
                if k in ("sensory", "nutrition", "source", "aliases"):
                    data[k] = {}
                else:
                    data[k] = []
            else:
                v_clean = v.strip("'\"")
                data[k] = v_clean

    return data, body


def is_junk_ingredient(ing):
    if not isinstance(ing, str):
        return True
    ing_lower = ing.lower().strip()
    if not ing_lower or "ingrediente principal" in ing_lower or ing_lower.startswith("ingrediente_"):
        return True
    return False


def is_collection_file(filepath):
    filename = os.path.basename(filepath)
    if filename == "README.md":
        return True
    if filename.startswith("recetas_"):
        return True
    return False


def audit_dishes(base_dir="site/src/content/dishes"):
    pattern = os.path.join(base_dir, "**/*.md")
    all_files = sorted(glob.glob(pattern, recursive=True))

    # Exclude READMEs and collection indexes
    files = [f for f in all_files if not is_collection_file(f)]
    collection_files = [f for f in all_files if is_collection_file(f)]

    total = len(files)
    prep_time_count = 0
    main_ings_count = 0
    sensory_flavor_count = 0

    missing_prep_time = []
    junk_main_ings = []
    missing_sensory_flavor = []

    for filepath in files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        fm, _ = parse_frontmatter(content)

        # Check prep_time
        prep = fm.get("prep_time")
        if prep and str(prep).strip() and str(prep).strip() != "[Pendiente]":
            prep_time_count += 1
        else:
            missing_prep_time.append(filepath)

        # Check main_ingredients
        ings = fm.get("main_ingredients")
        if isinstance(ings, list) and len(ings) > 0:
            valid_ings = [i for i in ings if not is_junk_ingredient(i)]
            if len(valid_ings) > 0 and len(valid_ings) == len(ings):
                main_ings_count += 1
            else:
                junk_main_ings.append(filepath)
        else:
            junk_main_ings.append(filepath)

        # Check sensory.flavor
        sensory = fm.get("sensory")
        if isinstance(sensory, dict):
            flavor = sensory.get("flavor")
            if flavor and flavor != "[Pendiente]" and flavor != ["[Pendiente]"]:
                sensory_flavor_count += 1
            else:
                missing_sensory_flavor.append(filepath)
        else:
            missing_sensory_flavor.append(filepath)

    print("=" * 60)
    print("GOS DISH FRONTMATTER COVERAGE AUDIT")
    print("=" * 60)
    print(f"Total recipe dishes audited: {total} (excluding {len(collection_files)} collection/README files)")
    print(f"prep_time coverage:          {prep_time_count}/{total} ({prep_time_count / total * 100:.1f}%) [target: >= 365]")
    print(f"main_ingredients usable:    {main_ings_count}/{total} ({main_ings_count / total * 100:.1f}%) [target: >= 365]")
    print(f"sensory.flavor coverage:    {sensory_flavor_count}/{total} ({sensory_flavor_count / total * 100:.1f}%) [target: >= 355]")
    print("=" * 60)

    # Threshold checks (targets set relative to total recipe dishes)
    target_prep = 365
    target_ings = 365
    target_flavor = 355

    prep_ok = prep_time_count >= target_prep
    ings_ok = main_ings_count >= target_ings
    sensory_ok = sensory_flavor_count >= target_flavor

    passed = prep_ok and ings_ok and sensory_ok

    if not passed:
        print("\n[FAIL] Coverage thresholds not met!")
        if not prep_ok:
            print(f"  - prep_time needed {target_prep}, got {prep_time_count}")
        if not ings_ok:
            print(f"  - main_ingredients usable needed {target_ings}, got {main_ings_count}")
        if not sensory_ok:
            print(f"  - sensory.flavor needed {target_flavor}, got {sensory_flavor_count}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All dish frontmatter coverage thresholds met!")
        sys.exit(0)


if __name__ == "__main__":
    audit_dishes()

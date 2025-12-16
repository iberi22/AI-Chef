import os
import re
import yaml
import time
from pathlib import Path

# Placeholder for specific ingredient data (Simulated Knowledge Base)
# In production, this would be replaced by an LLM API call.
KNOWLEDGE_BASE = {
    "大蒜": {
        "scientific_name": "Allium sativum",
        "group": "Vegetable/Spice",
        "scientific_registry": {
            "family": "Amaryllidaceae",
            "genus": "Allium",
            "synonyms": ["Garlic", "Ajo"],
            "cultivars": ["Softneck", "Hardneck"]
        },
        "nutrition": {
            "calories": 149,
            "protein_g": 6.4,
            "fat_g": 0.5,
            "carbs_g": 33,
            "fiber_g": 2.1,
            "sugar_g": 1
        },
        "safety": {
            "score": 95,
            "concerns": [{"condition": "Heartburn", "risk": "High doses may cause heartburn."}]
        },
        "i18n": {
            "en": {"common_name": "Garlic", "culinary_intro": "Pungent bulb used as flavoring."},
            "es": {"common_name": "Ajo", "culinary_intro": "Bulbo acre usado como condimento."},
            "zh": {"common_name": "大蒜", "culinary_intro": "百合科葱属植物的地下鳞茎。"}
        }
    },
    # Add more mappings or use a robust lookup function
}

def load_stub(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        # Return parsed dict AND the raw string block to replace later
        return yaml.safe_load(match.group(1)), match.group(0), content
    return None, None, content

def enrich_stub(file_path, data):
    front_matter, raw_yaml_block, full_content = load_stub(file_path)
    if not front_matter:
        print(f"Skipping {file_path}: No Front Matter found.")
        return

    # Check matches in Knowledge Base (by ZH name or filename)
    # This logic detects the 'zh' name from i18n block
    zh_name = front_matter.get('i18n', {}).get('zh', {}).get('common_name', '')
    en_name = front_matter.get('i18n', {}).get('en', {}).get('common_name', '')

    lookup_key = zh_name if zh_name != "TODO" else en_name

    if lookup_key in KNOWLEDGE_BASE:
        info = KNOWLEDGE_BASE[lookup_key]

        # Update Fields
        front_matter['scientific_name'] = info['scientific_name']
        front_matter['group'] = info['group']

        # Registry
        front_matter['scientific_registry']['family'] = info['scientific_registry']['family']
        front_matter['scientific_registry']['genus'] = info['scientific_registry']['genus']
        front_matter['scientific_registry']['synonyms'] = info['scientific_registry']['synonyms']

        # Nutrition
        front_matter['nutrition_per_100g'].update(info['nutrition'])

        # Safety
        front_matter['safety_profile']['safety_score'] = info['safety']['score']
        front_matter['safety_profile']['concerns'] = info['safety']['concerns']

        # i18n merge
        for lang, vals in info['i18n'].items():
            if lang in front_matter['i18n']:
                front_matter['i18n'][lang].update(vals)

        # Dump back to YAML
        new_yaml = yaml.dump(front_matter, allow_unicode=True, sort_keys=False)

        # Replace in content by swapping the OLD raw block with NEW block
        # We wrap new yaml in --- lines to match regex group(0)
        # However, group(0) from regex includes the --- lines.
        # But yaml.dump does NOT include them by default (unless explicit).
        new_block = f"---\n{new_yaml.strip()}\n---"

        new_content = full_content.replace(raw_yaml_block, new_block)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Enriched: {file_path}")
    else:
        # print(f"No data for: {lookup_key}")
        pass

def process_pending_folder():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pending_dir = os.path.join(base_dir, 'ingredients', 'pending_review')

    for root, dirs, files in os.walk(pending_dir):
        for file in files:
            if file.endswith(".md"):
                enrich_stub(os.path.join(root, file), None)

if __name__ == "__main__":
    process_pending_folder()

import os
import re

# Protocol Template
STUB_TEMPLATE = """---
name: "{name}"
scientific_name: "TODO"
group: "Uncategorized"
image: "../../images/placeholder.jpg"

# --- Internationalization ---
i18n:
  en:
    common_name: "{en_name}"
    other_names: []
  es:
    common_name: "{es_name}"
    other_names: []
  zh:
    common_name: "{zh_name}"
    other_names: []

# --- Scientific Registry ---
scientific_registry:
  family: "TODO"
  genus: "TODO"
  synonyms: []
  cultivars: []

# --- Nutrition (per 100g) ---
portions:
  default_g: 100
nutrition_per_100g:
  calories: 0
  protein_g: 0
  fat_g: 0
  carbs_g: 0
  fiber_g: 0
  sugar_g: 0

# --- Micronutrients ---
micronutrients:
  vitamin_c_mg: 0
  potassium_mg: 0
  magnesium_mg: 0

# --- Active Compounds ---
active_compounds: []

# --- Safety & Allergy Profile ---
safety_profile:
  safety_score: 50
  concerns: []

allergy_profile:
  risk_level: "Unknown"
  allergens: []
  prevalence_percent: 0

# --- Sensory Profile ---
sensory_profile:
  taste_notes: []
  texture_notes: []
  spice_level: 0

embedding_version: 2
last_updated: "{date}"
---

# {name}

## Description
*Aun no hay descripción científica para este ingrediente.*
"""

def is_chinese_char(char):
    return '\u4e00' <= char <= '\u9fff'

def guess_language_fields(raw_name):
    """
    Returns a dict with en_name, es_name, zh_name pre-filled
    based on the input script.
    Notes:
    - If Chinese, put in zh_name.
    - If Latin, put in es_name (default for this repo so far) AND en_name (as placeholder).
    - The "name" field should be Latin for filename compatibility.
    """
    has_chinese = any(is_chinese_char(c) for c in raw_name)

    fields = {
        "en_name": "TODO",
        "es_name": "TODO",
        "zh_name": "TODO",
        "name": raw_name # Fallback
    }

    if has_chinese:
        fields["zh_name"] = raw_name
        # For filename/main name, we might want pinyin or remain unicode?
        # The normalize_name function handles the filename safety.
        # For the YAML 'name' field, keep original for now or TODO?
        fields["name"] = raw_name
    else:
        # Assume Spanish/English overlap for now
        fields["es_name"] = raw_name
        fields["name"] = raw_name

    return fields

def normalize_name(name):
    """Normalize filename from ingredient name."""
    # Remove chars that are unsafe for filenames
    safe = re.sub(r'[^\w\s-]', '', name).strip().lower()
    return re.sub(r'[-\s]+', '_', safe)

def batch_create_stubs():
    import datetime
    today = datetime.date.today().isoformat()

    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    harvest_file = os.path.join(base_dir, 'scripts', 'ingredients_harvested.txt')
    ingredients_dir = os.path.join(base_dir, 'ingredients')
    pending_dir = os.path.join(ingredients_dir, 'pending_review')

    os.makedirs(pending_dir, exist_ok=True)

    # Load existing ingredients to avoid duplicates
    existing_ingredients = set()
    for root, dirs, files in os.walk(ingredients_dir):
        for file in files:
            if file.endswith(".md"):
                # Simplistic check: filename match
                existing_ingredients.add(file.replace('.md', ''))

    # Read harvested list
    if not os.path.exists(harvest_file):
        print("No harvest file found. Run harvest_ingredients.py first.")
        return

    created_count = 0
    with open(harvest_file, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' not in line: continue

            # Format is "count: name"
            parts = line.split(':', 1)
            if len(parts) < 2: continue

            count = parts[0].strip()
            raw_name = parts[1].strip()

            if len(raw_name) < 2: continue

            # Stopwords/Noise filter
            if raw_name in ['sal', 'pimienta', 'agua', 'aceite', 'azúcar', 'sugar', 'salt', 'oil', 'water', 'sal y pimienta al gusto']:
                continue

            safe_name = normalize_name(raw_name)

            if safe_name in existing_ingredients:
                print(f"Skipping existing: {safe_name}")
                continue

            # Create Stub
            file_path = os.path.join(pending_dir, f"{safe_name}.md")
            if not os.path.exists(file_path):
                lang_data = guess_language_fields(raw_name.title())

                content = STUB_TEMPLATE.format(
                    name=lang_data['name'],
                    en_name=lang_data['en_name'],
                    es_name=lang_data['es_name'],
                    zh_name=lang_data['zh_name'],
                    date=today
                )
                with open(file_path, 'w', encoding='utf-8') as out:
                    out.write(content)
                print(f"Created stub: {safe_name}.md")
                created_count += 1
            else:
                existing_ingredients.add(safe_name)

    print(f"\nBatch complete. Created {created_count} new stubs in {pending_dir}")

if __name__ == "__main__":
    batch_create_stubs()

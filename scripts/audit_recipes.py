
import os
import frontmatter
import re

DISHES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dishes')

def audit_recipes():
    print(f"Auditing recipes in: {DISHES_DIR}")

    missing_analysis = []
    missing_nutrition_fm = []
    missing_micronutrients = []

    count = 0

    for root, dirs, files in os.walk(DISHES_DIR):
        for file in files:
            if file.endswith(".md"):
                count += 1
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, DISHES_DIR)

                try:
                    post = frontmatter.load(filepath)
                    content = post.content
                    metadata = post.metadata

                    # 1. Check Frontmatter Nutrition
                    if 'nutrition' not in metadata:
                        missing_nutrition_fm.append(rel_path)

                    # 2. Check "Análisis Detallado y Sabiduría Colectiva"
                    # Using regex to look for h2 with similar title
                    if not re.search(r'^##\s+.*?Análisis Detallado.*?', content, re.MULTILINE | re.IGNORECASE):
                        missing_analysis.append(rel_path)

                    # 3. Check Micronutrients in a table
                    # Looking for a table header or content that mentions "Vitamin" or "Compuestos Destacados"
                    if not (re.search(r'\|.*?Compuestos Destacados.*?\|', content, re.IGNORECASE) or
                            re.search(r'\|.*?Vitamina.*?\|', content, re.IGNORECASE)):
                        missing_micronutrients.append(rel_path)

                except Exception as e:
                    print(f"Error reading {rel_path}: {e}")

    print(f"\n--- AUDIT REPORT ({count} recipes scanned) ---")

    if missing_analysis:
        print(f"\n[MISSING] 'Análisis Detallado y Sabiduría Colectiva' ({len(missing_analysis)}):")
        for p in missing_analysis:
             print(f"  - {p}")
    else:
        print("\n[OK] All recipes have Analysis section.")

    if missing_micronutrients:
        print(f"\n[MISSING] Micronutrients info in table ({len(missing_micronutrients)}):")
        for p in missing_micronutrients:
             print(f"  - {p}")
    else:
        print("\n[OK] All recipes have Micronutrients info.")

    if missing_nutrition_fm:
        print(f"\n[MISSING] Frontmatter 'nutrition' field ({len(missing_nutrition_fm)}):")
        for p in missing_nutrition_fm:
             print(f"  - {p}")

    # Summary for User
    if not missing_analysis and not missing_micronutrients and not missing_nutrition_fm:
         print("\n✅ All recipes are compliant with the new protocol!")
    else:
         print("\n⚠️  Some recipes need attention.")

if __name__ == "__main__":
    audit_recipes()

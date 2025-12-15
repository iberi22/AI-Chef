import os
import yaml
import re

def audit_recipes(base_dir):
    missing_front_matter = []
    missing_description = []
    missing_analysis_section = []
    missing_nutrition = []

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check Front Matter
                front_matter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                if not front_matter_match:
                    missing_front_matter.append(file_path)
                else:
                    try:
                        fm = yaml.safe_load(front_matter_match.group(1))
                        if 'description' not in fm:
                            missing_description.append(file_path)
                        if 'nutrition' not in fm:
                            missing_nutrition.append(file_path)
                    except yaml.YAMLError:
                        print(f"Error parsing YAML in {file_path}")

                # Check for "Análisis Detallado y Sabiduría Colectiva"
                if "Análisis Detallado y Sabiduría Colectiva" not in content:
                    missing_analysis_section.append(file_path)

    print(f"Total files missing Front Matter: {len(missing_front_matter)}")
    for f in missing_front_matter:
        print(f"  - {f}")

    print(f"\nTotal files missing Description (but have FM): {len(missing_description)}")
    for f in missing_description:
        print(f"  - {f}")

    print(f"\nTotal files missing Analysis Section: {len(missing_analysis_section)}")
    for f in missing_analysis_section:
        print(f"  - {f}")

if __name__ == "__main__":
    audit_recipes(r"e:\scripts-python\AI-Chef\dishes\colombian")

import os
import re
from collections import Counter

def harvest_ingredients(base_dir):
    ingredient_counter = Counter()

    # Headers to look for (Spanish, English, Chinese)
    # "必备原料和工具" is used in HowToCook
    header_pattern = re.compile(r'##\s+.*?(?:Ingredientes|Ingredients|必备原料和工具|原料)(.*?)(?:##|---)', re.DOTALL | re.IGNORECASE)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md") and file != "README.md":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Find Ingredients section
                    match = header_pattern.search(content)
                    if match:
                        ing_block = match.group(1)
                        lines = ing_block.split('\n')
                        for line in lines:
                            line = line.strip()
                            if line.startswith('-') or line.startswith('*'):
                                # Cleaning logic
                                # 1. Remove bullet
                                cleaned = re.sub(r'^[-*]\s*', '', line)
                                # 2. Remove typical quantity patterns (100g, 1 cup, 1/2) - tricky for Chinese
                                # For now, split by common delimiters to assume the first part is the name or name + qty

                                # Remove text in parenthesis (often variants or notes)
                                cleaned = re.sub(r'[\(（].*?[\)）]', '', cleaned)

                                # Split by common separators to isolate main item
                                # Spanish/English often use commas. Chinese might not.
                                parts = re.split(r'[,，]', cleaned)
                                candidate = parts[0].strip()

                                # Basic noise filter
                                if len(candidate) > 1 and not candidate[0].isdigit():
                                     # Remove quantity info if it appears at start?
                                     # E.g. "100g Tomato" -> "Tomato"
                                     # This regex attempts to strip leading numbers/units
                                     candidate = re.sub(r'^[\d\s\./]+(?:g|kg|ml|l|oz|lb|cup|taza|cda|tsp|tbsp|克|毫升|个|只|瓣|块|根)?\s*', '', candidate, flags=re.IGNORECASE)

                                     if candidate:
                                        ingredient_counter[candidate.lower()] += 1
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    print(f"Total unique ingredients found: {len(ingredient_counter)}")
    print("\nTop 50 Ingredients found:")
    for ing, count in ingredient_counter.most_common(50):
        print(f"{count}: {ing}")

    # Save to file
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ingredients_harvested.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
         for ing, count in ingredient_counter.most_common():
             f.write(f"{count}: {ing}\n")
    print(f"\nSaved list to {output_file}")

if __name__ == "__main__":
    # Go up one level from 'scripts' to root, then into 'dishes'
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dishes_path = os.path.join(project_root, "dishes")
    if os.path.exists(dishes_path):
        harvest_ingredients(dishes_path)
    else:
        print(f"Dishes directory not found at {dishes_path}")

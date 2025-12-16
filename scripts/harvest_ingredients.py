import os
import re
from collections import Counter

def harvest_ingredients(base_dir):
    ingredient_counter = Counter()

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md") and "README" not in file and "PLAN" not in file:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    lines = content.split('\n')
                    capturing = False

                    # 1. Identify start of ingredients section
                    for line in lines:
                        # Clean header check
                        if re.match(r'^##\s+.*?(?:Ingredientes|Ingredients|必备原料和工具|原料|食材)', line, re.IGNORECASE):
                            capturing = True
                            continue

                        # Stop if we hit next header or metadata separator
                        if capturing:
                            if line.strip().startswith('##') or line.strip().startswith('---'):
                                capturing = False
                                continue

                            # Valid list item check
                            stripped = line.strip()
                            if stripped.startswith('-') or stripped.startswith('*'):
                                # Cleaning logic
                                # 1. Remove bullet
                                cleaned = re.sub(r'^[-*]\s*', '', stripped)

                                # 2. Filter out Markdown formatting used for headers inside lists
                                if cleaned.startswith('**') or cleaned.startswith('#'):
                                    continue

                                # 3. Content in parenthesis
                                cleaned = re.sub(r'[\(（].*?[\)）]', '', cleaned)

                                # 4. Split by separators
                                parts = re.split(r'[,，:：]', cleaned)
                                candidate = parts[0].strip()

                                # 5. Quantity removal (improved)
                                # Remove leading digits/fractions/units
                                candidate = re.sub(r'^[\d\s\./½¼¾]+(?:g|kg|ml|l|oz|lb|cup|taza|vaso|cda|tsp|tbsp|gramos|litros|onzas|libras|克|毫升|个|只|瓣|块|根|把|勺|大勺|小勺|片|条|段|适量|少许)?\s*', '', candidate, flags=re.IGNORECASE)

                                # 6. Utensil/Noise filter keywords
                                noise_keywords = [
                                    'olla', 'sartén', 'licuadora', 'horno', 'bowl', 'cuchillo', 'tabla', 'pan', 'pot', 'blender', 'knife', 'board',
                                    '锅', '碗', '盆', '勺', '注：', '注意', '可选', 'opcional', 'optional', 'para servir', 'for serving', 'ingredients:', 'ingredientes:',
                                    'el yaml permite', 'enriquecimiento sensorial', 'imágenes libres', 'compatibilidad', 'licencia abierta', 'clasificación sensorial'
                                ]
                                if any(kw in candidate.lower() for kw in noise_keywords):
                                    continue

                                if len(candidate) > 1 and len(candidate) < 50 and not candidate[0].isdigit():
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

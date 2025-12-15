import os
import re
from collections import Counter

def harvest_ingredients(base_dir):
    ingredient_counter = Counter()

    # Regex to capture content after a dash in the Ingredientes section
    # This is a heuristic and might need refinement
    ing_pattern = re.compile(r'^- (?:[\d\./]+(?:\s?g|kg|lb|oz|taza|cda|cdta|ml)?\s+)?(.+?)(?:,|$|\(|$)', re.MULTILINE)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find Ingredients section
                match = re.search(r'##\s+.*?Ingredientes(.*?)(?:##|---)', content, re.DOTALL | re.IGNORECASE)
                if match:
                    ing_block = match.group(1)
                    # Find list items
                    lines = ing_block.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('-'):
                            # Try to extract the name
                            # Remove quantity if obvious (digits at start)
                            cleaned = re.sub(r'^- ([0-9/.]+\s?[a-zA-Z]*\s)?', '', line)
                            # Remove text in parenthesis
                            cleaned = re.sub(r'\s*\(.*?\)', '', cleaned)
                            # Simple cleanup
                            cleaned = cleaned.split(',')[0].strip().lower()
                            if cleaned and len(cleaned) > 2:
                                ingredient_counter[cleaned] += 1

    print("Top 50 Ingredients found:")
    for ing, count in ingredient_counter.most_common(50):
        print(f"{count}: {ing}")

    # Save to file
    with open('ingredients_harvested.txt', 'w', encoding='utf-8') as f:
         for ing, count in ingredient_counter.most_common():
             f.write(f"{count}: {ing}\n")

if __name__ == "__main__":
    harvest_ingredients(r"e:\scripts-python\AI-Chef\dishes\colombian")

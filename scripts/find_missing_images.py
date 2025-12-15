
import os
import frontmatter

DISHES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dishes', 'colombian')

def find_missing_images():
    print(f"Searching for recipes without local images in: {DISHES_DIR}")

    missing_images = []

    for root, dirs, files in os.walk(DISHES_DIR):
        for file in files:
            if file.endswith(".md") and file != "README.md":
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, DISHES_DIR)

                # Check for images folder next to the markdown
                recipe_dir = os.path.dirname(filepath)
                images_dir = os.path.join(recipe_dir, 'images')

                has_local_image = False
                if os.path.exists(images_dir):
                    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                    if image_files:
                        has_local_image = True

                if not has_local_image:
                    # Double check frontmatter for external images but prioritize local check for "completeness"
                    try:
                        post = frontmatter.load(filepath)
                        # We want local images for the pack
                        missing_images.append({
                            'path': rel_path,
                            'title': post.metadata.get('title', 'Unknown Title'),
                            'region': post.metadata.get('region', 'Unknown Region'),
                            'abs_path': filepath
                        })
                    except Exception:
                        pass

    print(f"\nFound {len(missing_images)} recipes without local images.\n")
    return missing_images

if __name__ == "__main__":
    missing = find_missing_images()
    for m in missing[:20]: # Show first 20
        print(f"MISSING: {m['title']} ({m['path']})")

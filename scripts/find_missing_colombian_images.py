
import os

def find_missing_colombian_images():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, 'dishes', 'colombian') # Target only Colombian recipes

    missing_files = []

    print(f"Scanning {target_dir} for missing images...\n")

    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md") and file != "README.md":
                # Check for image files in the same directory OR in 'images' subdir
                has_image = False
                # Check current dir
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')) and f != file:
                        has_image = True
                        break

                # Check images subdir if not found
                if not has_image:
                    images_path = os.path.join(root, 'images')
                    if os.path.isdir(images_path):
                        for f in os.listdir(images_path):
                            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                                has_image = True
                                break

                if not has_image:
                    full_path = os.path.join(root, file)
                    missing_files.append(full_path)
                    print(full_path)

    print(f"\nFound {len(missing_files)} recipes missing images.")

if __name__ == "__main__":
    find_missing_colombian_images()

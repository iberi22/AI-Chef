import os

def find_missing_images():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dishes_dir = os.path.join(base_dir, 'dishes')

    missing_count = 0
    total_count = 0

    print(f"Scanning {dishes_dir} for missing images...\n")

    for root, dirs, files in os.walk(dishes_dir):
        for file in files:
            if file.endswith(".md") and file != "README.md":
                total_count += 1
                # Check for image files in the same directory
                # Common extensions: .jpg, .png, .jpeg, .webp
                has_image = False
                for f in files:
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')) and f != file:
                        has_image = True
                        break

                if not has_image:
                    missing_count += 1
                    # print(f"[MISSING] {os.path.join(root, file)}")

    print(f"\nSummary:")
    print(f"Total Recipes: {total_count}")
    print(f"Missing Images: {missing_count}")
    print(f"Coverage: {((total_count - missing_count)/total_count)*100:.1f}%")

if __name__ == "__main__":
    find_missing_images()

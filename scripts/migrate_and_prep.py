
import os
import shutil
import re
import unicodedata

def normalize_name(name):
    # Normalize unicode characters to closest ASCII representation
    nfkd_form = unicodedata.normalize('NFKD', name)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8')
    return only_ascii.lower().replace(' ', '_').replace('ñ', 'n')

def migrate_recipes():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    colombian_dir = os.path.join(base_dir, 'dishes', 'colombian')

    # List of relative paths (from colombian dir) to process
    targets = [
        'snacks/deditos_de_queso.md',
        'snacks/pandeyuca.md',
        'panes/pan_aliñado.md',
        'panes/pan_de_yuca.md',
        'pacifica/tollo_ahumado/tollo_ahumado.md', # Check if folder exists
        'pacifica/tollo_ahumado.md'
    ]

    print(f"Starting migration in {colombian_dir}...\n")

    for target in targets:
        full_path = os.path.join(colombian_dir, target)

        # Check if file exists
        if not os.path.exists(full_path):
            # Check if it might already be in a folder (e.g. if target was file but it's now dir/file)
            # This logic is simple: if the file path provided doesn't exist, we skip or try to find it.
            # But let's assume the list is mostly flat files we want to migrate.
            # For the subdirectories found in the `find_missing` output (like amazon/casabe/casabe.md),
            # they are ALREADY in folders. We only need to ensure `images` folder exists.

            # Use a simpler heuristic: check if the 'basename' exists as a folder
            dir_name = os.path.splitext(os.path.basename(target))[0]
            parent_dir = os.path.dirname(full_path)
            potential_dir = os.path.join(parent_dir, dir_name) # e.g. snacks/buñuelo -> snacks/bunuelo (normalized?)

            # Actually, per plan, we want to NORMALIZE the folder name.
            normalized_dir_name = normalize_name(dir_name)
            target_folder = os.path.join(parent_dir, normalized_dir_name)

            if os.path.exists(target_folder) and os.path.isdir(target_folder):
                 print(f"Folder already exists for {target}: {target_folder}")
                 # Ensure images dir exists
                 images_dir = os.path.join(target_folder, 'images')
                 os.makedirs(images_dir, exist_ok=True)
                 continue

            # If neither file nor folder found easily, verify specifically
            print(f"Skipping {target} (not found as flat file)")
            continue

        # If it is a file, migrate it
        if os.path.isfile(full_path):
            file_name = os.path.basename(full_path)
            name_no_ext = os.path.splitext(file_name)[0]
            new_folder_name = normalize_name(name_no_ext)

            parent_dir = os.path.dirname(full_path)
            new_folder_path = os.path.join(parent_dir, new_folder_name)

            # Create new folder
            os.makedirs(new_folder_path, exist_ok=True)

            # Move file
            new_file_path = os.path.join(new_folder_path, file_name)
            shutil.move(full_path, new_file_path)

            # Create images folder
            images_dir = os.path.join(new_folder_path, 'images')
            os.makedirs(images_dir, exist_ok=True)

            print(f"Migrated: {target} -> {new_folder_path}")

if __name__ == "__main__":
    migrate_recipes()

import os
import hashlib

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def remove_duplicates():
    # 1. Existing photos for Club Que
    existing_photos = [f'assets/{f}' for f in os.listdir('assets') if f.startswith('live-') and f.endswith('.jpg')]
    
    # 2. New photos in que_new
    que_new_dir = 'assets/que_new'
    if not os.path.exists(que_new_dir):
        print("que_new directory not found.")
        return
        
    new_photos = [f'{que_new_dir}/{f}' for f in os.listdir(que_new_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Compare hashes
    new_hashes = {}
    for path in new_photos:
        new_hashes[get_file_hash(path)] = path
        
    duplicates_removed = 0
    for path in existing_photos:
        h = get_file_hash(path)
        if h in new_hashes:
            print(f"Found duplicate: {path} is same as {new_hashes[h]}")
            os.remove(path) # Remove the old one in assets/
            duplicates_removed += 1
            
    print(f"Removed {duplicates_removed} duplicate photos from assets/.")

if __name__ == "__main__":
    remove_duplicates()

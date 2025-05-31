import os
import json
from paxlib.hash_object import hash_object

PAX_DIR = ".pax"
INDEX_PATH = os.path.join(PAX_DIR, "index")

def add(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Hash the object and get its SHA-1
    sha1 = hash_object(file_path)

    # Load current index
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r") as f:
            index = json.load(f)
    else:
        index = {}

    # Add/update entry
    index[file_path] = sha1

    # Save updated index
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f)

    print(f"Added {file_path}")

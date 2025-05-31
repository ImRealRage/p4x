import os
import hashlib
import zlib
import json

PAX_DIR = ".pax"
INDEX_PATH = os.path.join(PAX_DIR, "index")

def write_tree():
    """
    Write a tree object using the contents of the index.

    This function reads the staging index and creates a tree object
    with all tracked files. It stores the tree in the object store 
    and returns its SHA1 hash.
    
    Returns
    -------
    str
        The SHA1 hash of the created tree object.
    """
    if not os.path.exists(INDEX_PATH):
        print("Index is empty or missing.")
        return

    with open(INDEX_PATH, "r") as f:
        index = json.load(f)

    entries = []

    for file_path, sha1 in sorted(index.items()):
        mode = "100644"  # Regular file
        entry = f"{mode} {file_path}".encode() + b'\0' + bytes.fromhex(sha1)
        entries.append(entry)

    tree_data = b''.join(entries)
    header = f"tree {len(tree_data)}\0".encode()
    full_tree = header + tree_data
    sha1 = hashlib.sha1(full_tree).hexdigest()

    dir_name = os.path.join(PAX_DIR, "objects", sha1[:2])
    file_name = sha1[2:]
    os.makedirs(dir_name, exist_ok=True)

    with open(os.path.join(dir_name, file_name), "wb") as f:
        f.write(zlib.compress(full_tree))

    print(sha1)
    return sha1

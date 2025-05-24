import os
import hashlib
import zlib
from paxlib.hash_object import hash_object

PAX_DIR = ".pax"

def write_tree(directory="."):
    """
    Write a tree object from the current directory's contents.

    This function iterates through the files in the specified directory, 
    skipping the .pax directory and any non-file entries. Each file is 
    hashed using the `hash_object` function, and a tree object is created 
    with a mode of 100644 for each file. The tree object is stored in the 
    .pax/objects directory, and its SHA1 hash is returned.

    Parameters
    ----------
    directory : str, optional
        The path to the directory to process. Defaults to the current directory.

    Returns
    -------
    str
        The SHA1 hash of the created tree object.
    """
    entries = []

    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)

        # Skip the .pax directory
        if entry == PAX_DIR or not os.path.isfile(full_path):
            continue

        # Hash the file if not already done
        sha1 = hash_object(full_path)

        # File mode is always 100644 (regular file) for now
        mode = "100644"
        entry_data = f"{mode} {entry}".encode() + b'\0' + bytes.fromhex(sha1)
        entries.append(entry_data)

    tree_data = b''.join(entries)
    header = f"tree {len(tree_data)}\0".encode()
    full_tree = header + tree_data
    sha1 = hashlib.sha1(full_tree).hexdigest()

    # Store it in .pax/objects/
    dir_name = os.path.join(PAX_DIR, "objects", sha1[:2])
    file_name = sha1[2:]
    os.makedirs(dir_name, exist_ok=True)

    with open(os.path.join(dir_name, file_name), "wb") as f:
        f.write(zlib.compress(full_tree))

    print(sha1)
    return sha1

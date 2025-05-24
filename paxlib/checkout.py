import os
import zlib

PAX_DIR = ".pax"

def read_object(sha1):
    path = os.path.join(PAX_DIR, "objects", sha1[:2], sha1[2:])
    with open(path, "rb") as f:
        compressed = f.read()
    return zlib.decompress(compressed)

def read_tree(tree_sha1):
    obj = read_object(tree_sha1)
    header_end = obj.find(b'\0')
    body = obj[header_end+1:]

    i = 0
    entries = []
    while i < len(body):
        space_index = body.find(b' ', i)
        null_index = body.find(b'\0', space_index)
        mode = body[i:space_index].decode()
        name = body[space_index+1:null_index].decode()
        sha1 = body[null_index+1:null_index+21].hex()
        entries.append((mode, name, sha1))
        i = null_index + 21
    return entries

def checkout(commit_sha1):
    """
    Checkout a specific commit by restoring files from the associated tree.

    This function reads a commit object identified by the given SHA1 hash, 
    extracts the tree SHA1, and then reads the corresponding tree object. 
    The tree object contains entries for each file, which are read and 
    written back to the working directory, effectively restoring the files
    to the state of the specified commit.

    Parameters
    ----------
    commit_sha1 : str
        The SHA1 hash of the commit to checkout.
    """
    # Step 1: Read the commit
    commit_data = read_object(commit_sha1)
    header_end = commit_data.find(b'\0')
    content = commit_data[header_end+1:]
    lines = content.decode().split("\n")
    tree_sha1 = None

    for line in lines:
        if line.startswith("tree "):
            tree_sha1 = line.split()[1]
            break

    if not tree_sha1:
        print("No tree found in commit.")
        return

    # Step 2: Read the tree and restore files
    entries = read_tree(tree_sha1)
    for mode, name, sha1 in entries:
        blob_data = read_object(sha1)
        blob_header_end = blob_data.find(b'\0')
        file_content = blob_data[blob_header_end+1:]
        with open(name, "wb") as f:
            f.write(file_content)
        print(f"Checked out {name}")

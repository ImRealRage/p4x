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

def restore_tree(tree_sha1):
    entries = read_tree(tree_sha1)
    for mode, name, sha1 in entries:
        blob_data = read_object(sha1)
        blob_header_end = blob_data.find(b'\0')
        file_content = blob_data[blob_header_end+1:]
        with open(name, "wb") as f:
            f.write(file_content)
        print(f"Checked out {name}")

def resolve_ref(ref):
    path = os.path.join(PAX_DIR, ref)
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return ref  # If not a ref, assume it's a raw commit hash

def checkout(target):
    # Branch name or commit hash
    ref_path = os.path.join(PAX_DIR, "refs", "heads", target)
    if os.path.exists(ref_path):
        with open(os.path.join(PAX_DIR, "HEAD"), "w") as f:
            f.write(f"ref: refs/heads/{target}\n")
        commit_sha1 = resolve_ref(f"refs/heads/{target}")
    else:
        commit_sha1 = target  # assume direct commit SHA

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

    restore_tree(tree_sha1)
    print(f"Checked out {target} ({commit_sha1[:7]})")

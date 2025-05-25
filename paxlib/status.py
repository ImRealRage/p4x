import os
import hashlib
import zlib
from paxlib.checkout import read_object, read_tree
from paxlib.repo import get_head

PAX_DIR = ".pax"

def hash_file_contents(path):
    with open(path, "rb") as f:
        data = f.read()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()

def status():
    # Step 1: Find HEAD commit
    head_ref = get_head()
    ref_path = os.path.join(PAX_DIR, head_ref)
    if not os.path.exists(ref_path):
        print("No commits yet.")
        return

    with open(ref_path) as f:
        commit_sha = f.read().strip()

    # Step 2: Read the commit and its tree
    commit_data = read_object(commit_sha)
    header_end = commit_data.find(b'\0')
    body = commit_data[header_end+1:].decode()
    tree_sha = None

    for line in body.split("\n"):
        if line.startswith("tree "):
            tree_sha = line.split()[1]
            break

    if not tree_sha:
        print("Malformed commit (no tree)")
        return

    tree_entries = {name: sha for _, name, sha in read_tree(tree_sha)}
    wd_files = {
        f: hash_file_contents(f)
        for f in os.listdir(".")
        if os.path.isfile(f) and f != __file__ and not f.startswith(PAX_DIR)
    }

    # Step 3: Compare
    print(f"On branch {head_ref.split('/')[-1]}")
    print("")

    added = []
    modified = []
    deleted = []

    for name in wd_files:
        if name not in tree_entries:
            added.append(name)
        elif wd_files[name] != tree_entries[name]:
            modified.append(name)

    for name in tree_entries:
        if name not in wd_files:
            deleted.append(name)

    if added:
        print("Untracked files:")
        for f in added:
            print(f"  {f}")
        print()

    if modified:
        print("Modified files:")
        for f in modified:
            print(f"  {f}")
        print()

    if deleted:
        print("Deleted files:")
        for f in deleted:
            print(f"  {f}")
        print()

    if not (added or modified or deleted):
        print("Working directory clean.")

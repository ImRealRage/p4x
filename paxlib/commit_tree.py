import hashlib
import os
import zlib
import time

PAX_DIR = ".pax"

def commit_tree(tree_hash, message, parent=None, author="You <you@example.com>"):
    """
    Commit a tree object with a given message.
    """
    lines = [f"tree {tree_hash}"]
    if parent:
        lines.append(f"parent {parent}")

    timestamp = int(time.time())
    timezone = time.strftime('%z') or '+0000'

    lines.append(f"author {author} {timestamp} {timezone}")
    lines.append(f"committer {author} {timestamp} {timezone}")
    lines.append("")
    lines.append(message)

    commit_data = "\n".join(lines).encode()
    header = f"commit {len(commit_data)}\0".encode()
    full_commit = header + commit_data

    sha1 = hashlib.sha1(full_commit).hexdigest()
    dir_name = os.path.join(PAX_DIR, "objects", sha1[:2])
    file_name = sha1[2:]
    os.makedirs(dir_name, exist_ok=True)

    with open(os.path.join(dir_name, file_name), "wb") as f:
        f.write(zlib.compress(full_commit))

    # Update the current branch (HEAD)
    head_path = os.path.join(PAX_DIR, "HEAD")
    if os.path.exists(head_path):
        with open(head_path, "r") as f:
            ref = f.read().strip()
        
        if ref.startswith("ref:"):
            ref_path = os.path.join(PAX_DIR, ref[5:])  # strip "ref: "
            with open(ref_path, "w") as f:
                f.write(sha1)

    print(sha1)
    return sha1

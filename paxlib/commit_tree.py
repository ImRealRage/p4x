import hashlib
import os
import zlib
import time

PAX_DIR = ".pax"

def get_head_ref():
    """Return the ref path from HEAD if it's a symbolic ref."""
    head_path = os.path.join(PAX_DIR, "HEAD")
    with open(head_path) as f:
        content = f.read().strip()
        if content.startswith("ref: "):
            return content[5:]
    return None  # Detached HEAD

def update_ref(ref, sha):
    """Write the given commit SHA to the specified ref."""
    path = os.path.join(PAX_DIR, ref)
    with open(path, "w") as f:
        f.write(sha + "\n")

def commit_tree(tree_hash, message, parent=None, author="You <you@example.com>"):
    lines = [f"tree {tree_hash}"]
    if parent:
        lines.append(f"parent {parent}")

    timestamp = int(time.time())
    date_str = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(timestamp))

    lines.append(f"author {author} {timestamp} +0000")
    lines.append(f"committer {author} {timestamp} +0000")
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

    # Update branch ref if HEAD is symbolic
    head_ref = get_head_ref()
    if head_ref:
        update_ref(head_ref, sha1)

    print(sha1)
    return sha1

import hashlib
import os
import zlib
import time

PAX_DIR = ".pax"

def commit_tree(tree_hash, message, parent=None, author="You <you@example.com>"):
    """
    Commit a tree object with a given message.

    Parameters
    ----------
    tree_hash : str
        The hash of the tree object to commit.
    message : str
        The commit message.
    parent : str, optional
        The hash of the parent commit. If not given, this is the initial commit.
    author : str, optional
        The author of the commit in the format "Name <email>"

    Returns
    -------
    str
        The hash of the new commit.
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

    print(sha1)
    return sha1

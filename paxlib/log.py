import os
import zlib
import time

PAX_DIR = ".pax"

def read_object(sha1):
    path = os.path.join(PAX_DIR, "objects", sha1[:2], sha1[2:])
    with open(path, "rb") as f:
        compressed_data = f.read()
    return zlib.decompress(compressed_data)

def parse_commit(data):
    lines = data.decode().split("\n")
    meta = {}
    i = 0

    while i < len(lines) and lines[i]:
        if lines[i].startswith("tree "):
            meta["tree"] = lines[i][5:].strip()
        elif lines[i].startswith("parent "):
            meta["parent"] = lines[i][7:].strip()
        elif lines[i].startswith("author "):
            meta["author"] = lines[i][7:].strip()
        elif lines[i].startswith("committer "):
            meta["committer"] = lines[i][10:].strip()
        i += 1

    message = "\n".join(lines[i+1:]).strip()
    meta["message"] = message
    return meta

def format_timestamp(ts_str):
    try:
        timestamp = int(ts_str)
        return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(timestamp))
    except:
        return ts_str  # fallback in case of error

def log(commit_sha1):

    """
    Display the commit history starting from the given commit SHA1.

    This function reads and parses the commit object identified by the given 
    SHA1 hash, prints the commit information including the author, date, and 
    message, and then moves to the parent commit to repeat the process, 
    effectively displaying the commit log in reverse chronological order.

    Parameters
    ----------
    commit_sha1 : str
        The SHA1 hash of the commit from which to start the log.
    """
    
    while commit_sha1:
        data = read_object(commit_sha1)
        header_end = data.find(b'\0')
        content = data[header_end+1:]

        commit = parse_commit(content)

        # Split author correctly to extract timestamp (last 2 parts)
        author_full = commit["author"]
        author_parts = author_full.rsplit(" ", 2)
        name_email = author_parts[0]
        timestamp = author_parts[1]

        print(f"commit {commit_sha1}")
        print(f"Author: {name_email}")
        print(f"Date:   {format_timestamp(timestamp)}\n")
        print(f"    {commit['message']}\n")

        commit_sha1 = commit.get("parent")

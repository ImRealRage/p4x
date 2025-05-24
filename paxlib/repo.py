import os

PAX_DIR = ".pax"

def init_repo():
    """Initialize a new Pax repository in the current directory."""
    if os.path.exists(PAX_DIR):
        print("Repository already initialized.")
        return

    os.makedirs(os.path.join(PAX_DIR, "objects"))
    os.makedirs(os.path.join(PAX_DIR, "refs", "heads"))

    # Set HEAD to point to master
    with open(os.path.join(PAX_DIR, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    # Create empty branch file for master (will be updated after first commit)
    with open(os.path.join(PAX_DIR, "refs", "heads", "master"), "w") as f:
        f.write("")

    print(f"Initialized empty Pax repository in {os.path.abspath(PAX_DIR)}")

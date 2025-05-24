import os

PAX_DIR = ".pax"

def init_repo():
    """Initialize a new Pax repository in the current directory.

    This function creates a `.pax` directory in the current working directory
    and initializes it as a Pax repository. If the repository has already been
    initialized, it does nothing.

    """
    if os.path.exists(PAX_DIR):
        print("Repository already initialized.")
        return

    os.makedirs(os.path.join(PAX_DIR, "objects"))
    os.makedirs(os.path.join(PAX_DIR, "refs", "heads"))

    with open(os.path.join(PAX_DIR, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    print(f"Initialized empty Pax repository in {os.path.abspath(PAX_DIR)}")

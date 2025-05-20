import os

PAX_DIR = ".pax"

def init_repo():
    if os.path.exists(PAX_DIR):
        print("Repository already initialized.")
        return

    os.makedirs(os.path.join(PAX_DIR, "objects"))
    os.makedirs(os.path.join(PAX_DIR, "refs", "heads"))

    with open(os.path.join(PAX_DIR, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    print(f"Initialized empty Pax repository in {os.path.abspath(PAX_DIR)}")

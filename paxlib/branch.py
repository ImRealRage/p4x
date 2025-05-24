import os

def branch(name):
    # Read HEAD to get current commit SHA
    with open(".pax/HEAD") as f:
        ref = f.read().strip()
    
    if ref.startswith("ref:"):
        ref_path = os.path.join(".pax", ref[5:])
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                sha = f.read().strip()
        else:
            print("Error: current branch not found")
            return
    else:
        # Detached HEAD
        sha = ref

    branch_path = os.path.join(".pax", "refs", "heads", name)
    with open(branch_path, "w") as f:
        f.write(sha)

    print(f"Branch '{name}' created at {sha}")

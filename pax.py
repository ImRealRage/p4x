import sys
from paxlib.repo import init_repo
from paxlib.hash_object import hash_object
from paxlib.write_tree import write_tree
from paxlib.commit_tree import commit_tree
from paxlib.log import log
from paxlib.checkout import checkout



def main():
    if len(sys.argv) < 2:
        print("Usage: pax <command>")
        return

    command = sys.argv[1]

    if command == "init":
        init_repo()
    
    elif command == "hash-object":
        if len(sys.argv) < 3:
            print("Usage: pax hash-object <file>")
        else:
            hash_object(sys.argv[2]) 
    
    elif command == "write-tree":
        write_tree()
        
    elif command == "commit-tree":
        try:
            tree_hash = sys.argv[2]
            if sys.argv[3] == "-m":
                message = sys.argv[4]
                commit_tree(tree_hash, message)
            else:
                print("Usage: pax commit-tree <tree-hash> -m \"message\"")
        except IndexError:
            print("Usage: pax commit-tree <tree-hash> -m \"message\"")
            
    elif command == "log":
        if len(sys.argv) < 3:
            print("Usage: pax log <commit-sha>")
        else:
            log(sys.argv[2])
            
    elif command == "checkout":
        if len(sys.argv) != 3:
            print("Usage: pax checkout <commit-sha>")
        else:
            checkout(sys.argv[2])
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

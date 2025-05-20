import sys
from paxlib.repo import init_repo
from paxlib.hash_object import hash_object

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
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

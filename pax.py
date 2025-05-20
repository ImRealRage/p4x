import sys
from paxlib.repo import init_repo

def main():
    if len(sys.argv) < 2:
        print("Usage: pax <command>")
        return

    command = sys.argv[1]

    if command == "init":
        init_repo()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()

import sys

from client.gpu_client import run_client
from server.gpu_server import run_server


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['-s', '-c']:
        print("Usage: python main.py [-s|-c]")
        print("  -s: run as server")
        print("  -c: run as client")
        sys.exit(1)

    if sys.argv[1] == '-s':
        run_server()
    else:
        run_client()

if __name__ == "__main__":
    main()
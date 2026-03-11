from tqdm import tqdm
import signal
import sys
import time

shutdown_request: bool = False


def graceful_shutdown(signum, fname):
    global shutdown_request
    print(f"\nReceived signal {signum} , initating graceful shutdown\n")
    shutdown_request = True


signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)


def main():
    print("app started\n")
    while not shutdown_request:
        print("active...")
        time.sleep(1)
    print("graceful shutdown complete")
    sys.exit(0)


if __name__ == "__main__":
    main()

import json
import socket
from datetime import datetime, timezone

HOST = "127.0.0.1"
PORT = 5280


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print(f"Listening for 6-node Castleberry Bloom packets on udp://{HOST}:{PORT} (Ctrl+C to stop)...")

    try:
        while True:
            data, addr = sock.recvfrom(65535)
            ts = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
            raw = data.decode("utf-8", errors="replace")
            print(f"\n[{ts}] Packet from {addr[0]}:{addr[1]} ({len(data)} bytes)")
            try:
                parsed = json.loads(raw)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(raw)
    except KeyboardInterrupt:
        print("\nListener stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()

import socket
import threading
import time

HOST = "127.0.0.1"
PORT_LISTEN = 5280
PORT_TARGET = 5282

def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT_LISTEN))
    print(f"[Listener] Bound to {HOST}:{PORT_LISTEN} - waiting for CML packets...")
    
    while True:
        data, addr = sock.recvfrom(4096)
        print(f"[Listener] Received {len(data)} bytes from {addr}: {data.decode('utf-8', errors='ignore')}")
        break
    sock.close()

def udp_sender():
    time.sleep(1) # Give listener time to bind
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    test_packet = "<cml_packet node=\"test_node\" freq=\"528.0\">\n  <payload>Test Mycelial Transmission</payload>\n</cml_packet>"
    print(f"[Sender] Broadcasting test packet to {HOST}:{PORT_LISTEN}...")
    sock.sendto(test_packet.encode('utf-8'), (HOST, PORT_LISTEN))
    sock.close()

if __name__ == "__main__":
    t_listener = threading.Thread(target=udp_listener, daemon=True)
    t_sender = threading.Thread(target=udp_sender, daemon=True)
    
    t_listener.start()
    t_sender.start()
    
    time.sleep(2)
    print("[Test] UDP socket forwarder verification complete.")

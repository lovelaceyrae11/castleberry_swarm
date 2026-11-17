import socket
import xml.etree.ElementTree as ET

def start_listener(port=5282):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', port))
    
    print(f"\n[✓] CML Parser Listener active on port {port}. Waiting for telemetry...")
    print("=" * 60)
    
    try:
        while True:
            data, addr = sock.recvfrom(2048)
            packet_str = data.decode()
            
            try:
                # Strip XML namespace tags for clean parsing
                if 'xmlns' in packet_str or 'cml:' in packet_str:
                    clean_str = packet_str.replace('cml:', '')
                else:
                    clean_str = packet_str
                    
                root = ET.fromstring(clean_str)
                cycle = root.get('cycle')
                freq = root.get('frequency')
                axis = root.get('axis')
                taurus = root.get('taurus_coord')
                scorpio = root.get('scorpio_coord')
                balance = root.get('balance')
                
                print(f"[RX PARSED] Cycle: {cycle.strip()} | Freq: {freq} | Axis: {axis}")
                print(f"            Coords -> Taurus: {taurus} | Scorpio: {scorpio}")
                print(f"            Token Gate Balance: {balance} BLOOM")
                print("-" * 60)
            except Exception as e:
                print(f"[!] Parse Exception ({e}). Raw Packet: {packet_str}")
                
    except KeyboardInterrupt:
        print("\n[✓] Parser listener stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    start_listener()

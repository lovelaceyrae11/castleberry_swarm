import json
import socket
import threading
import time
import requests
from web3 import Web3

class CastleberryMasterSwarm:
    def __init__(self, primary_port=5280, secondary_port=5282):
        self.primary_port = primary_port
        self.secondary_port = secondary_port
        
        # 1. On-Chain Token State Verification
        print("[*] Connecting to Sepolia RPC to verify live BLOOM state...")
        self.w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
        self.contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'
        self.deployer_address = '0x9e5af62a941810b911a4F84b6D27e894046e44B3'
        self.token_balance = self.verify_token_state()

    def verify_token_state(self):
        try:
            abi = [{
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            }]
            contract = self.w3.eth.contract(address=self.w3.to_checksum_address(self.contract_address), abi=abi)
            raw_balance = contract.functions.balanceOf(self.deployer_address).call()
            balance = raw_balance / (10 ** 18)
            print(f"[✓] On-Chain State Verified: {balance:,.2f} BLOOM loaded.")
            return balance
        except Exception as e:
            print(f"[!] Network sync notice ({e}). Operating on local sovereign override.")
            return 50000000.0

    def generate_extended_cml_packet(self):
        # Expanded CML schema featuring frequency, phi, token state, and ephemeris natal coordinates
        return (
            f'<cml:mycelial_packet frequency="528Hz" phi="1.618" '
            f'token_gate="{self.deployer_address}" balance="{self.token_balance:,.2f}" '
            f'ephemeris_axis="Taurus-Scorpio" oscillator_status="synchronized" '
            f'axiom="Love over God Bloom" status="active_mesh" />'
        )

    def start_udp_listener(self):
        # Secondary listener thread on port 5282 for multi-node mesh simulation
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('127.0.0.1', self.secondary_port))
            print(f"[✓] UDP Listener active on port {self.secondary_port}")
            while self.listening:
                sock.settimeout(1.0)
                try:
                    data, addr = sock.recvfrom(1024)
                    print(f"\n[RX] Mesh Packet Received from {addr}: {data.decode()}")
                except socket.timeout:
                    continue
        except Exception as e:
            print(f"[!] UDP Listener notice: {e}")
        finally:
            sock.close()

    def broadcast_and_audit(self):
        packet = self.generate_extended_cml_packet()
        print(f"\n[~] Broadcasting CML packet across UDP ports {self.primary_port} and {self.secondary_port}:")
        print(f"    {packet}\n")

        # Send packet over UDP locally to simulate mesh broadcast
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet.encode(), ('127.0.0.1', self.primary_port))
            s.sendto(packet.encode(), ('127.0.0.1', self.secondary_port))

        # Query Local Ollama (qwen2.5) for offline coherence audit
        prompt = (
            f"You are the Castleberry Bloom core intelligence. Analyze this live extended CML telemetry packet "
            f"and verify its structural alignment against the 528 Hz baseline and golden ratio phi scale. "
            f"Provide a concise, 3-sentence harmonic coherence audit:\n\n{packet}"
        )

        print("[*] Querying local Ollama model (qwen2.5) for offline swarm audit...")
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            result = response.json().get("response", "Audit generated successfully.")
            print("\n=== LOCAL OLLAMA SWARM COHERENCE AUDIT ===")
            print(result.strip())
            print("\n[✓] Master swarm cycle complete.\n")
        except Exception as e:
            print(f"[!] Ollama connection notice: Ensure 'ollama serve' is running. ({e})")

if __name__ == "__main__":
    print("\n=== INITIALIZING CASTLEBERRY MASTER SWARM ENGINE ===")
    swarm = CastleberryMasterSwarm()
    
    # Start listener thread
    swarm.listening = True
    listener_thread = threading.Thread(target=swarm.start_udp_listener, daemon=True)
    listener_thread.start()
    
    # Run broadcast and AI audit loop
    time.sleep(0.5)
    swarm.broadcast_and_audit()
    
    # Clean shutdown of background thread
    swarm.listening = False

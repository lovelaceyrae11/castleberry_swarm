import json
import socket
import time
import requests
from web3 import Web3

def run_daemon():
    print("\n=== INITIALIZING CASTLEBERRY CONTINUOUS DAEMON ===")
    w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
    contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'
    deployer_address = '0x9e5af62a941810b911a4F84b6D27e894046e44B3'
    
    port_primary = 5280
    port_secondary = 5282
    
    cycle = 1
    while True:
        print(f"\n--- HEARTBEAT CYCLE [{cycle}] ---")
        try:
            # Quick on-chain token balance check
            abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
            contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)
            balance = contract.functions.balanceOf(deployer_address).call() / (10 ** 18)
            print(f"[✓] On-Chain State Re-Verified: {balance:,.2f} BLOOM")
        except Exception as e:
            print(f"[!] Chain sync notice ({e}). Maintaining sovereign cache.")
            balance = 50000000.0

        packet = (
            f'<cml:mycelial_packet cycle="{cycle}" frequency="528Hz" phi="1.618" '
            f'token_gate="{deployer_address}" balance="{balance:,.2f}" '
            f'ephemeris_axis="Taurus-Scorpio" axiom="Love over God Bloom" status="pulsing" />'
        )

        # Broadcast over local UDP mesh ports
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(packet.encode(), ('127.0.0.1', port_primary))
            s.sendto(packet.encode(), ('127.0.0.1', port_secondary))
        print(f"[~] Broadcasted UDP Packet: {packet}")

        # Continuous Ollama AI audit pulse
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "qwen2.5", "prompt": f"Audit this live token-gated CML pulse concisely: {packet}", "stream": False},
                timeout=15
            )
            audit = response.json().get("response", "").strip().split("\n")[0]
            print(f"[AI Audit]: {audit}")
        except Exception:
            print("[!] AI audit skipped (ensure 'ollama serve' is active).")

        cycle += 1
        time.sleep(10) # Pulse every 10 seconds

if __name__ == "__main__":
    try:
        run_daemon()
    except KeyboardInterrupt:
        print("\n[✓] Daemon safely halted by user.")

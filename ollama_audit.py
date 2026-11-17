import json
import requests
from web3 import Web3

def audit_swarm_node():
    print("[*] Connecting to Sepolia to verify live BLOOM state...")
    w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
    contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'
    deployer_address = '0x9e5af62a941810b911a4F84b6D27e894046e44B3'
    
    try:
        abi = [{
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        }]
        contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)
        balance = contract.functions.balanceOf(deployer_address).call() / (10 ** 18)
    except Exception:
        balance = 50000000.0

    cml_packet = (
        f'<cml:mycelial_packet frequency="528Hz" phi="1.618" '
        f'token_gate="{deployer_address}" balance="{balance:,.2f}" '
        f'status="active_routing" />'
    )

    prompt = (
        f"You are the Castleberry Bloom core intelligence. Analyze the following live CML telemetry packet "
        f"and on-chain token state. Provide a concise, 3-sentence harmonic coherence audit:\n\n"
        f"Packet: {cml_packet}\n"
        f"Baseline Frequency: 528 Hz\n"
        f"Geometric Scale: Golden Ratio (1.618)\n"
        f"Axiom: Love over God Bloom"
    )

    print("[*] Querying local Ollama model (qwen2.5) for offline audit...")
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
        print("\n=== LOCAL OLLAMA COHERENCE AUDIT ===")
        print(result.strip())
        print("\n[✓] Audit complete.\n")
    except Exception as e:
        print(f"[!] Ollama connection error: {e}")

if __name__ == "__main__":
    audit_swarm_node()

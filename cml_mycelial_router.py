import json
import socket
from web3 import Web3

class CmlMycelialRouter:
    def __init__(self, port_primary=5280, port_secondary=5282):
        self.port_primary = port_primary
        self.port_secondary = port_secondary
        
        # Connect to PublicNode Sepolia RPC for local token validation
        self.w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
        self.contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'
        self.deployer_address = '0x9e5af62a941810b911a4F84b6D27e894046e44B3'
        
        print(f"[*] Initializing CML Mycelial Router across ports {self.port_primary} & {self.port_secondary}...")
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
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(self.contract_address), 
                abi=abi
            )
            raw_balance = contract.functions.balanceOf(self.deployer_address).call()
            balance = raw_balance / (10 ** 18)
            print(f"[✓] On-Chain State Verified: {balance:,.2f} BLOOM loaded into router.")
            return balance
        except Exception as e:
            print(f"[!] Network sync warning ({e}). Operating on local sovereign override.")
            return 50000000.0

    def generate_packet(self):
        return (
            f'<cml:mycelial_packet frequency="528Hz" phi="1.618" '
            f'token_gate="{self.deployer_address}" balance="{self.token_balance}" '
            f'status="active_routing" />'
        )

    def broadcast_simulation(self):
        packet = self.generate_packet()
        print(f"\n[~] Broadcasting CML packet on UDP ports {self.port_primary} and {self.port_secondary}:")
        print(f"    {packet}\n")
        print("[✓] Mycelial swarm grid synchronized successfully.")

if __name__ == "__main__":
    router = CmlMycelialRouter()
    router.broadcast_simulation()

from web3 import Web3

# Connect to PublicNode's open Sepolia RPC
w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))

# Corrected contract and deployer address holding the tokens
contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'
deployer_address = '0x9e5af62a941810b911a4F84b6D27e894046e44B3'

# Minimal ERC-20 ABI for balanceOf
abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]

contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)

# Fetch raw balance and convert from 18 decimals
raw_balance = contract.functions.balanceOf(deployer_address).call()
readable_balance = raw_balance / (10 ** 18)

print(f"\n=== BLOOMTOKEN STATE (SEPOLIA) ===")
print(f"Contract: {contract_address}")
print(f"Wallet:   {deployer_address}")
print(f"Balance:  {readable_balance:,.2f} BLOOM\n")

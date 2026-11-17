from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'

# Common derivation/test addresses or alternative accounts in MetaMask
# Let's check your primary address and other common testnet indices if available
candidate_addresses = [
    '0x0641aAb3669C79fEC18594037648261863Ae27aA',
    # If you had another account active during Remix deployment, add it here
]

abi = [{
    "constant": True,
    "inputs": [{"name": "_owner", "type": "address"}],
    "name": "balanceOf",
    "outputs": [{"name": "balance", "type": "uint256"}],
    "type": "function"
}]

contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)

print("\n=== SCANNING WALLET BALANCES ===")
for addr in candidate_addresses:
    balance = contract.functions.balanceOf(addr).call() / (10 ** 18)
    print(f"Address {addr}: {balance:,.2f} BLOOM")

print("")

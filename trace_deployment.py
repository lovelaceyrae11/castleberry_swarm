from web3 import Web3

# Connect to PublicNode's open Sepolia RPC
w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))

contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'

abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": False, "name": "value", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]

contract = w3.eth.contract(address=w3.to_checksum_address(contract_address), abi=abi)

total_supply = contract.functions.totalSupply().call() / (10 ** 18)
print(f"\n--- BLOOMTOKEN DEPLOYMENT TRACE ---")
print(f"Total Supply verified on-chain: {total_supply:,.2f} BLOOM")

# Get current block and scan the last 40,000 blocks (within the 50k limit)
latest_block = w3.eth.block_number
from_block = max(0, latest_block - 40000)

print(f"Scanning mint logs from block {from_block} to {latest_block}...")
events = contract.events.Transfer.get_logs(
    from_block=from_block,
    to_block='latest',
    argument_filters={'from': '0x0000000000000000000000000000000000000000'}
)

for event in events:
    recipient = event['args']['to']
    amount = event['args']['value'] / (10 ** 18)
    print(f"Minted {amount:,.2f} BLOOM to address: {recipient}")

print("")

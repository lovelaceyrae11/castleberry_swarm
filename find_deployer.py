from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))
contract_address = '0xDB90B1A8aF557de8d9F195627d475f983634ECBd'

# Let's check if there are any other addresses or if we can inspect the creation transaction directly
# If you have another address you suspect, type it in below or paste it here:
print("To find your tokens, do you have another Ethereum address you were logged into in MetaMask when you deployed?")

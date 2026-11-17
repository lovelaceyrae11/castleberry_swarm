from web3 import Web3
import json

SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
BLOOM_TOKEN_ADDRESS = "0xDB90B1A8aF557de8d9F195627d475f983634ECBd"

ERC20_ABI = json.loads('''[
    {"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},
    {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"type":"function"},
    {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}
]''')

def read_token_state(wallet_address):
    w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    
    if not w3.is_connected():
        print("[Error] Failed to connect to Sepolia network RPC.")
        return
    
    token_address = w3.to_checksum_address(BLOOM_TOKEN_ADDRESS)
    user_address = w3.to_checksum_address(wallet_address)
    
    contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
    
    try:
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call() / (10 ** decimals)
        balance_raw = contract.functions.balanceOf(user_address).call()
        balance_formatted = balance_raw / (10 ** decimals)
    except Exception as e:
        print(f"[Error querying contract state]: {e}")
        return

    print(f"\n=== BloomToken Live State (Sepolia) ===")
    print(f"Token Name:    {name}")
    print(f"Symbol:        {symbol}")
    print(f"Decimals:      {decimals}")
    print(f"Total Supply:  {total_supply:,.2f} {symbol}")
    print(f"Contract:      {token_address}")
    print(f"\n--- Holder Status ---")
    print(f"Wallet:        {user_address}")
    print(f"Token Balance: {balance_formatted:,.2f} {symbol}")

if __name__ == "__main__":
    my_wallet = "0x0641aAb3669C79fEC18594037648261863Ae27aA" 
    read_token_state(my_wallet)

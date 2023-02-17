from solcx import compile_standard, install_solc

install_solc("0.8.0")

import json
#from sqlalchemy import false, true
from web3 import Web3

# Read the contents of the SimpleStorage.sol contract file
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile the Solidity contract using the solcx package
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

# Save the compiled contract's bytecode and ABI to a local file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Extract the bytecode and ABI from the compiled contract
# bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Connect to ganache
w3 = Web3(Web3.HTTPProvider("http://0.0.0.0:8545"))
chain_id = 1337
my_addres = "0x0b5f26B6Af7E68141aF752cAdceB25847C159377"
private_key = "0xbab0495136e3873d980cb98f001a2dee530bd8f6add74836cd2badd3967a0aed"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the nonce
nonce = w3.eth.getTransactionCount(my_addres)

# Our token 
name = "VSToken"
symbol = "VST"
decimals = 2
total_supply = 1000000

# Build a transaction
transaction = SimpleStorage.constructor(name, symbol, decimals, total_supply).build_transaction(
    {"chainId": chain_id, "from": my_addres, "nonce": nonce}
)

# Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


while(1):
    print("------------------------------------- \n Izbornik:\n 1: Provjeri stanje racuna \n 2: Mint \n 3: Burn \n 4: Posalji tokene \n 5: Posalji tokene (from-to) \n 6: Izlaz")
    unos = input("\nVaš odabir: ")
    if(unos == 1):
        print("1")
    elif(unos == 2):
        print("2")
    elif(unos == 3):
        print("3")
    elif(unos == 4):
        print("4")
    elif(unos == 5):
        print("5")
    elif(unos == 6):
        print("Izlaz! Hvala na upotrebi!")
        exit()
    else:
        print("Krivi unos! Pokušajte ponovno!")

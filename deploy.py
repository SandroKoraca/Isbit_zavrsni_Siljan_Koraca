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
my_address = "0x982eDCC34eCc6f5213fb75b03BFAfFAEEf3cF3A9"
private_key = "0xbd988abe5f314e084434269f7b6bfeb4d0a616703692c489e9cc9819b0e21434"

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the nonce
nonce = w3.eth.getTransactionCount(my_address)

# Our token 
name = "VSToken"
symbol = "VST"
total_supply = 1000

# Build a transaction
transaction = SimpleStorage.constructor(name, symbol, total_supply).build_transaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# Sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


contract_address = tx_receipt['contractAddress']
SimpleStorage2 = w3.eth.contract(address = contract_address, abi=abi)

while(1):
    print("\n------------------------------------- \nIzbornik:\n 1: Provjeri stanje racuna \n 2: Mint \n 3: Burn \n 4: Posalji tokene \n 5: Posalji tokene (from-to) \n 6: Izlaz")
    unos = input("\nVas odabir: ")
    if(unos == "1"): #Provjeri stanje racuna
        unos2= input("\nOdaberite zelite li provjeriti svoju ili tudju adresu: \n 1: Svoja \n 2: Tudja \nVas odabir:")
        if(unos2 == "1"): #Provjera svoje adrese
            ballance = SimpleStorage2.functions.ballanceOf(my_address).call()
            print("\nStanje vaseg racuna:", ballance)
        elif(unos2 == "2"):
            address = input("\nUnesite adresu: ")
            ballance = SimpleStorage2.functions.ballanceOf(address).call()
            print("\nStanje tudjeg racuna:", ballance)
        else:
            print("\nKrivi unos! Pokušajte ponovno!")
    elif(unos == "2"): #Mint
        unos2= input("\nOdaberite zelite li dodati tokene na svoj ili tudji racun: \n 1: Svoj \n 2: Tudji \nVas odabir:")
        if(unos2 == "1"): #Dodavanje na svoj racun
            numberForMint = int(input("\nKoliko tokena zelite dodati(mint): "))
            mint = SimpleStorage2.functions.mint(my_address, numberForMint).transact({'from': my_address})
            ballance = SimpleStorage2.functions.ballanceOf(my_address).call()
            print("\nNovo stanje: ", ballance)
        elif(unos2 == "2"): #Dodavanje na tudji racun
            numberForMint = int(input("\nKoliko tokena zelite dodati(mint): "))
            address = input("Unesite adresu: ")
            mint = SimpleStorage2.functions.mint(address, numberForMint).transact({'from': my_address})
            ballance = SimpleStorage2.functions.ballanceOf(address).call()
            print("\nNovo stanje: ", ballance)
        else:
            print("\nKrivi unos! Pokušajte ponovno!")
    elif(unos == "3"): #Burn
        unos2= input("\nOdaberite zelite li smanjiti tokene na svojem ili tudjem racunu: \n 1: Svoj \n 2: Tudji \nVas odabir:")
        if(unos2 == "1"): #Smanjivanje na svoj racun
            numberForBurn = int(input("\nKoliko tokena zelite smanjiti(burn): "))
            burn = SimpleStorage2.functions.burn(my_address, numberForBurn).transact({'from': my_address})
            ballance = SimpleStorage2.functions.ballanceOf(my_address).call()
            print("\nNovo stanje: ", ballance)
        elif(unos2 == "2"): #Smanjivanje na tudji racun
            numberForBurn = int(input("\nKoliko tokena zelite smanjiti(burn): "))
            address = input("Unesite adresu: ")
            burn = SimpleStorage2.functions.burn(address, numberForBurn).transact({'from': my_address})
            ballance = SimpleStorage2.functions.ballanceOf(address).call()
            print("\nNovo stanje: ", ballance)
        else:
            print("\nKrivi unos! Pokušajte ponovno!")
    elif(unos == "4"): #Posalji tokene
        tokenForSend = int(input("\nKoliko tokena zelite poslati: "))
        address = input("Unesite adresu: ")
        SimpleStorage2.functions.transfer(address,tokenForSend).transact({'from': my_address})
        ballance = SimpleStorage2.functions.ballanceOf(my_address).call()
        print("\nVase novo stanje: ", ballance)
    elif(unos == "5"): #Posalji tokene (from-to)
        tokenForSend = int(input("\nKoliko tokena se salje: "))
        addressFrom = input("Unesite adresu iz koje se salje: ")
        addressTo = input("Unesite adresu na koju se salje: ")
        SimpleStorage2.functions.transferFrom(addressFrom, addressTo,tokenForSend).transact({'from': my_address})
        ballanceFrom = SimpleStorage2.functions.ballanceOf(addressFrom).call()
        ballanceTo = SimpleStorage2.functions.ballanceOf(addressTo).call()
        print("\nNovo stanje na adresi ",addressFrom,": ", ballanceFrom)
        print("Novo stanje na adresi ",addressTo,": ", ballanceTo)
    elif(unos == "6"): #Izlaz
        print("\nIzlaz! Hvala na upotrebi!")
        exit()
    else: #krivi unos
        print("\nKrivi unos! Pokušajte ponovno!")

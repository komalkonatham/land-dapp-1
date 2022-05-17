from web3 import Web3,HTTPProvider
import json

def connect_Blockchain_register(acc):
    blockchain_address="http://127.0.0.1:8545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    contract_address="0xE5406abA43387423fb71414c50a33C85D44DF442"
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

contract,web3=connect_Blockchain_register('0xFa25C5636123719fb21997a7EcC9b7ca3F983C16')
# tx_hash=contract.functions.registerUser(123,'maddy'.encode('utf-8'),1234).transact()
# web3.eth.waitForTransactionReceipt(tx_hash)

state=contract.functions.loginUser(123,1234).call()
print(state)

state=contract.functions.loginUser(123,123).call()
print(state)
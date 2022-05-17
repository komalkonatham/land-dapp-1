from flask import Flask, redirect,render_template,request
import json
from web3 import Web3,HTTPProvider
app=Flask(__name__)

propertyContractAddress='0xb27C8CCCe24dfe250e01a8a6D5Be8e92842687B6'
registerContractAddress='0xB77299E6860F38F9a85D4aD07EE13F5deDda4ed1'

def connect_with_register_blockchain(acc):
    blockchain_address="http://127.0.0.1:8545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    contract_address=registerContractAddress
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

def connect_with_property_blockchain(acc):
    blockchain_address="http://127.0.0.1:8545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/property.json'
    contract_address=propertyContractAddress
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/registerProperty')
def registerPropertyPage():
    return render_template('registerproperty.html')

@app.route('/dashboard')
def dashboardPage():
    contract,web3=connect_with_property_blockchain(0)
    _propertyId,_ownerId,_propertyData=contract.functions.viewProperties().call()
    print(_propertyId,_ownerId,_propertyData)
    data=[]
    try:
        for i in range(len(_propertyData)):
            dummy=[]
            dummy.append(_propertyId[i])
            dummy.append(_ownerId[i][:-1])
            dummy.append(_propertyData)
    except:
        data=['NA','NA','NA']
    return render_template('dashboard.html',len=len(data),dashboard_data=data)

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    name=request.form['username']
    id=request.form['userid']
    password=request.form['password']
    print(name,id,password)
    contract,web3=connect_with_register_blockchain(0)
    tx_hash=contract.functions.registerUser(int(id),name,int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return (redirect('/login'))

@app.route('/loginUser',methods=['POST','GET'])
def loginUser():
    id=int(request.form['userid'])
    password=int(request.form['password'])
    print(id,password)
    contract,web3=connect_with_register_blockchain(0)
    state=contract.functions.loginUser(id,password).call()
    print(state)
    return (redirect('/dashboard'))

if __name__=="__main__":
    app.run(debug=True)
from flask import Flask, redirect,render_template,request, session
import json
from web3 import Web3,HTTPProvider
import smtplib
import random

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
smtpObj=smtplib.SMTP('smtp.gmail.com',587)
smtpObj.starttls()
smtpObj.login('landblockchain56@gmail.com','m@keskilled')
otp_created=0

app=Flask(__name__)
app.secret_key='makeskilled'

propertyContractAddress='0x40f68d86C36AFf7eD404Ee9Ca01fF88Cb2b51897'
registerContractAddress='0xE8997b931a1b044395f3f4D56aEF0e4BD35Af1E2'

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

@app.route('/linkEmail')
def linkEmailPage():
    return render_template('linkemail.html')

@app.route('/linkEmailForm',methods=['POST','GET'])
def linkEmailForm():
    global otp_created
    emailId=request.form['emailId']
    otp_created=random.randint(1800,9999)
    
    msg = MIMEMultipart()
    msg['From'] = 'landblockchain56@gmail.com'
    msg['To'] = emailId
    msg['Subject']= 'Your OTP as User registration'
    msg.attach(MIMEText("OTP to register: "+str(otp_created), 'plain'))
    text = msg.as_string()
    smtpObj.sendmail('landblockchain56@gmail.com',msg['To'],text)
    session['email']=emailId
    return render_template('otp.html')

@app.route('/verifyOTPForm',methods=['POST','GET'])
def verifyOTPFormPage():
    global otp_created
    otp=request.form['otp']
    if int(otp)==otp_created:
        return redirect('/register')
    else:
        return redirect('/linkEmail')
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
    contract,web3=connect_with_register_blockchain(0)
    _ids,_names,_emails=contract.functions.viewUsers().call()
    print(_ids,_names,_emails)

    data=[]
    try:
        for i in range(len(_propertyId)):
            dummy=[]
            ownerIndex=_ids.index(_ownerId[i][-1])
            dummy.append(_propertyId[i])
            dummy.append(_names[ownerIndex])
            dummy.append(_propertyData[i])
            data.append(dummy)
    except:
        data=['NA','NA','NA']
    return render_template('dashboard.html',len=len(data),dashboard_data=data)

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
    name=request.form['username']
    id=request.form['userid']
    password=request.form['password']
    email=session['email']
    print(name,id,password)
    contract,web3=connect_with_register_blockchain(0)
    tx_hash=contract.functions.registerUser(int(id),email,name,int(password)).transact()
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

@app.route('/propertyOTPForm',methods=['POST','GET'])
def propertyOTPFormPage():
    global otp_created
    otp=request.form['otp']
    if int(otp)==otp_created:
        propertyId=session['propertyId']
        ownerId=session['ownerId']
        propertyData=session['propertyData']
        contract,web3=connect_with_property_blockchain(0)
        tx_hash=contract.functions.registerProperty(propertyId,ownerId,propertyData).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return (redirect('/dashboard'))
    else:
        return (redirect('/dashboard'))

@app.route('/registerPropertyForm',methods=['POST','GET'])
def registerPropertyForm():
    global otp_created
    propertyId=int(request.form['propertyId'])
    ownerId=int(request.form['ownerId'])
    propertyData=request.form['propertyData']
    print(propertyId,ownerId,propertyData)
    session['propertyId']=propertyId
    session['ownerId']=ownerId
    session['propertyData']=propertyData
    contract,web3=connect_with_register_blockchain(0)
    _ids,_names,_emails=contract.functions.viewUsers().call()
    print(_ids,_names,_emails)
    ownerIndex=_ids.index(ownerId)
    emailId=_emails[ownerIndex]
    otp_created=random.randint(1800,9999)
    
    msg = MIMEMultipart()
    msg['From'] = 'landblockchain56@gmail.com'
    msg['To'] = emailId
    msg['Subject']= 'Your OTP to register your property'
    msg.attach(MIMEText("OTP to register: "+str(otp_created), 'plain'))
    text = msg.as_string()
    smtpObj.sendmail('landblockchain56@gmail.com',msg['To'],text)
    session['email']=emailId
    return render_template('propertyotp.html')


if __name__=="__main__":
    app.run(debug=True)
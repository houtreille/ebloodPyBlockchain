from flask import Flask, json
from flask.templating import render_template
import mysql.connector
from werkzeug.exceptions import abort
from flask import Flask, render_template, request, url_for, flash, redirect
from ebloodCoin.blockchain.transaction.Transaction import Transaction
from flask.globals import session
from ebloodCoin.utils import SignatureUtils
from Tools.demo.mcast import receiver, sender
from ebloodCoin.proxy.proxyController import proxyController
from pyasn1.compat import integer

global wallet
proxy = proxyController()
app = Flask(__name__)
app.config["DEBUG"] = 'True'
app.config['SECRET_KEY'] = 'your secret key'



@app.route('/')
def index(): 
    
    connString =getConnectedWalletString()
    print('connString ' + connString )
    print(str(proxy.connectedWallet))
    return render_template('index.html', proxy = proxy)

@app.route('/createNewBlock', methods=('GET', 'POST')) 
def createNewBlock():
    
    if(proxy.getBlockchain().getSize() > 0 and not proxy.getBlockchain().getLastBlock().hash): 
        flash("last block not mined")
        print("last block not mined")
        return render_template('displayBlockChain.html', blockchain=proxy.blockchain.blockchain, proxy = proxy)
    else:
        if(proxy.getBlockchain().getSize() == 0):
             block =  proxy.createNewBlock(None)
        else:
             block =  proxy.createNewBlock(proxy.blockchain.getGenesisBlock().hash)
        proxy.addBlockToBlockchain(block)
    
    flash("Block {0} has been created".format(block.id),'sucess')
    return render_template('newBlock.html', block=block,title='New Block', proxy = proxy)


@app.route('/displayBlockChain')
def displayBlockChain():
    return render_template('displayBlockChain.html', blockchain=proxy.blockchain.blockchain, proxy = proxy)

@app.route('/hack')
def hackBlockChain():
    proxy.hackBlockChain()
    flash("Blockchain has been modified")
    return render_template('displayBlockChain.html', blockchain=proxy.blockchain.blockchain, proxy = proxy)


@app.route('/displayBlock/<int:id>/')
def displayBlock(id):
    block = proxy.blockchain.getBlock(id)
    if not block:
        abort(404)
    else:
        return render_template('displayBlock.html', block = block, proxy = proxy )
    
@app.route('/mineBlock/<int:id>/')
def mineBlock(id):
    block = proxy.blockchain.getBlock(id)
    block.mineBlock()
    
    flash("Block {0} has been mined, hash : {1}".format(block.id, block.hash),'sucess')
    return render_template('displayBlockChain.html', blockchain=proxy.blockchain.blockchain,  proxy = proxy)
 
@app.route('/addTransactionToBlock/<int:id>/', methods=('GET', 'POST')) 
def addTransactionToBlock(id):
    
    if request.method == 'POST':
        receiver = request.form['receiver']
        fundToTransfer = request.form['fundToTransfer']
        sender = request.form['sender']
        
        trans = Transaction(sender, [receiver], [fundToTransfer], None)
        
        trans.signTransaction(proxy.connectedWallet.privateKey)
        
        proxy.addTransactionToBlock( trans, id-1)
        return render_template('displayBlock.html', block = proxy.blockchain.getBlock(id-1) , proxy = proxy)
    else:
        block = proxy.blockchain.getBlock(id-1)
        return render_template('newTransaction.html', block=block, proxy = proxy)
        '''block = proxy.blockchain.getBlock(id)
        block.addTransaction(trans)'''
    

@app.route('/createWallet', methods=('GET', 'POST')) 
def createWallet():
    
    
    print("Create Wallet : " + request.method)
    
    if request.method == 'POST':
        name = request.form['walletName']
        
        password = request.form['walletpassword']
        
        file = request.form['keyFile']
        
        print("Wallet name : " + name + " " + password + " "  + file )
        
        proxy.createdWallet.setName(name)
        proxy.createdWallet.setPassword(password)
        
        SignatureUtils.exportAsFile(proxy.createdWallet.dict, 'PEM', name+"Private.PEM", name+"Public.PEM", password)
        
        
        return render_template('wallet/createWallet.html' , wallet = None)
        
    else:
        wallet = proxy.createWallet()
        
         
        session['walletPublicKey'] = wallet.getublicKeyAsStr()
        #proxy.persistWallet(wallet, path)    
    
        return render_template('wallet/createWallet.html' , wallet = wallet)
    


@app.route('/connectWallet', methods=('GET', 'POST')) 
def connectWallet():
    if request.method == 'POST':
        
        password = request.form['passwd']
        pemFilePath =    request.form['keyFile'] #"C:/Work/EclipseProjects/Python/pythonBlockchain/flaskProject/eblood/" +
        walletName =  pemFilePath[0:pemFilePath.rfind("Private.PEM")]
        
        proxy.connectedWallet =  proxy.retrieveWallet(app.root_path, walletName, password)
        
        
     
        return redirect(url_for("index"))
    else:
        return render_template('wallet/connectWallet.html', proxy = proxy)
    
    


@app.route('/dashboard') 
def dashboard():     
    labels = []
    values = []
    
    for key, value in proxy.connectedWallet.assetHistory.items():
        labels.append(key)
        values.append(value)
        
    legend = "Balance"
   
    return render_template('wallet/dashboard.html', values=values, legend=legend, labels=labels, proxy = proxy)


@app.route('/jumbo') 
def jumbo():     
    
    labels = []
    values = []
    
    for key, value in proxy.connectedWallet.assetHistory.items():
        labels.append(key)
        values.append(value)
        
    legend = "Balance"
    
    return render_template('wallet/jumbotron.html', values=values, legend=legend, labels=labels, proxy = proxy)

@app.route('/transferFund', methods=('GET', 'POST')) 
def transferFund():
    if request.method == 'POST':
        sender = proxy.connectedWallet
        #proxy.getWalletByName(request.form['sender'])
        receiver = proxy.getWalletByName(request.form['receiver'])
        fundToTransfer = float(request.form['fundToTransfer'])
        try:
            t1 = proxy.transferFunds(proxy.connectedWallet, [receiver], [fundToTransfer])
            proxy.addTransaction(t1)
            flash("{0} has been created".format(t1.hashId))
        except NameError as err:
            flash("{0}".format(err))    
            
            
        return redirect(url_for("index"))
        
    else:
        if(proxy.getBlockchain().getSize() == 0):
            block =  proxy.createNewBlock(None)
            proxy.addBlockToBlockchain(block)
            flash("Block {0} has been created".format(block.id),'success')
        else:
            block = proxy.blockchain.getLastBlock()
        
        return render_template('newTransaction.html', block=block, proxy = proxy)


   
def getConnectedWalletString():
    if proxy.connectedWallet:
        return  proxy.connectedWallet.name
    else:
        return 'Connect Wallet'
    
    
    
@app.route('/testAngular')
def testAngular(): 

    return render_template('angular/testAngular.html')    


@app.route('/index2')
def about(): 
    return render_template('index2.html')

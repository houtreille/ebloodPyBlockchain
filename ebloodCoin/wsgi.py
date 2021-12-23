from flask import Flask
from flask.templating import render_template
import mysql.connector
from werkzeug.exceptions import abort
from flask import Flask, render_template, request, url_for, flash, redirect
from ebloodCoin.proxy.proxyController import proxy
from ebloodCoin.blockchain.transaction.Transaction import Transaction
import json
import os
import base64

proxy = proxy()
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
    wallet = proxy.createWallet()
    wallet.setName('eblood')
    wallet.password = "Reuss1r+"
    path = wallet.name + ".txt"
    proxy.persistWallet(wallet, path)    
    
    return render_template('wallet/createWallet.html', wallet=wallet , proxy = proxy)
    
    



@app.route('/connectWallet', methods=('GET', 'POST')) 
def connectWallet():
    if request.method == 'POST':
        
        password = request.form['passwd']
        pemFilePath = "C:/Work/EclipseProjects/Python/pythonBlockchain/flaskProject/eblood/" +   request.form['keyFile']
        proxy.connectedWallet =  proxy.retrieveWallet(pemFilePath=pemFilePath, password=password)
        proxy.connectedWallet.setName(pemFilePath[1+pemFilePath.rfind("/"):pemFilePath.rfind("_")])
     
        return redirect(url_for("index"))
    else:
        return render_template('wallet/connectWallet.html', proxy = proxy)
    
    
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

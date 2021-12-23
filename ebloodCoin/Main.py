'''
Created on 6 Dec 2021

@author: administration
'''
from ebloodCoin.blockchain.Blockchain import Blockchain
from ebloodCoin.blockchain.Block import Block
from ebloodCoin.utils import HashingUtils
from ebloodCoin.test.testComponent import testBlock, testTransaction
from ebloodCoin.gui.HelloWorld import HelloWorld
import cherrypy
from ebloodCoin.proxy.proxyController import proxy
from ebloodCoin.blockchain.Wallet import Wallet
import base64
from ebloodCoin.blockchain.transaction.Transaction import Transaction

proxy = proxy()

if __name__ == '__main__':
    
    
    
    
    '''path = 'C:/Work/EclipseProjects/Python/pythonBlockchain/flaskProject/eblood/eblood_private.PEM'
    name = path[1+path.rfind("/"):path.rfind("_")]
    wallet = Wallet(name = 'C:/Work/EclipseProjects/Python/pythonBlockchain/flaskProject/eblood/eblood_private.PEM', initKey = False)
    wallet = wallet.retrieve('C:/Work/EclipseProjects/Python/pythonBlockchain/flaskProject/eblood/eblood_private.PEM', 'Reuss1r+')
    
    b1 = Block(0, 3, wallet.privateKey)
    tr = Transaction(['eblood'], ['eblood'], [1000], None)
    signature = tr.signTransaction(wallet.privateKey)
    sign64 = base64.b64encode(signature)'''
    
    
    
    '''blockChain = Blockchain()
    blockChain.printBlockChain()
    
    block = Block(0,2,3)
    block.mineBlock()
    print(block.calulateBlockHash())'''
   
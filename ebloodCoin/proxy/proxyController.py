'''
Created on 15 Dec 2021

@author: administration
'''
from ebloodCoin.blockchain.Blockchain import Blockchain
from ebloodCoin.blockchain.Block import Block
from ebloodCoin.blockchain.Wallet import Wallet


class proxy(object):
   

    def __init__(self):
        self.blockchain = Blockchain()
        self.connectedWallet = None
        
        
        
    def getBlockchain(self):
        return self.blockchain
    
    
    def createNewBlock(self, previousHashId = 0):
        if self.getBlockchain().getSize() == 0:
            block = Block(previousHashId)
        else:
            block = Block(self.getBlockchain().getLastBlock().hash)
            
        return block
        
        
    def addBlockToBlockchain(self, block):   
         self.blockchain.addBlock(block)
         block.id = self.blockchain.getSize()
         
    def signTransaction(self, trans, privateKey):     
        trans.signTransaction(privateKey)
         
         
    def addTransactionToBlock(self, trans, blockNb):
        self.blockchain.getBlock(blockNb).addTransaction(trans)
        
    def createWallet(self):
        return Wallet()    
    
    def retrieveWallet(self, pemFilePath, password):
        wallet = Wallet(name = pemFilePath, initKey = False)
        wallet = wallet.retrieve(pemFilePath, password)
        return wallet
    
        
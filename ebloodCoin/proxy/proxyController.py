from ebloodCoin.blockchain.transaction.Transaction import Transaction
#from ebloodCoin.blockchain import Block
from ebloodCoin.wallets.Wallet import Wallet
from ebloodCoin.blockchain.Blockchain import Blockchain
from ebloodCoin.blockchain.Block import Block
from ebloodCoin.blockchain.transaction.UTXo import UTXo
from flask.helpers import flash




class proxyController(object):
   

    def __init__(self):
        self.blockchain = Blockchain()
        self.connectedWallet = None
        self.createdWallet = None
        self.minerWallet =  Wallet("Miner", True, False)
        
    def getBlockchain(self):
        return self.blockchain
    
    def createNewBlock(self, previousHashId = 0):
        if self.getBlockchain().getSize() == 0:
            block = Block(previousHashId, creator=self.minerWallet)
        else:
            block = Block(self.getBlockchain().getLastBlock().hash, creator=self.minerWallet)
            
        return block
        
        
    def addBlockToBlockchain(self, block):   
         self.blockchain.addBlock(block)
         block.id = self.blockchain.getSize()-1
         
    def signTransaction(self, trans, privateKey):     
        trans.signTransaction(privateKey)
         
         
    def addTransaction(self, trans):
        
        if(self.getBlockchain().getSize() == 0):#genesisblock
            genesisBlock = self.createNewBlock("0")
            genesisBlock.addTransaction(trans)
            genesisBlock.mineBlock()
            genesisBlock.signBlock()
            self.addBlockToBlockchain(genesisBlock)
        
        elif (len(self.getBlockchain().getLastBlock().transactions) == Block.MAX_TRANS_NB or self.getBlockchain().getLastBlock().previousHashId == "0"):
            
            lastBlock = self.getBlockchain().getLastBlock()
            lastBlock.mineBlock()
            lastBlock.signBlock();
            
            newBlock = self.createNewBlock(lastBlock.hash)
            self.addBlockToBlockchain(newBlock)
            newBlock.addTransaction(trans)
            
        else:
            
            lastBlock = self.getBlockchain().getLastBlock() 
            lastBlock.addTransaction(trans)
              
            
         
    def addTransactionToBlock(self, trans, block):
        block.addTransaction(trans)
        
    def createWallet(self):
        self.createdWallet = Wallet()    
        return self.createdWallet
        
        
    def retrieveWallet(self, pemFilePath, name, password):
       
        wallet = Wallet(name, initKey = False)
        wallet = wallet.retrieve(pemFilePath, name, password)
        self.faucet(wallet)
        
        
        return wallet    
    
    def verifyBlockChain(self):
        
        
        lastblock = None
        
        for block in self.blockchain.blockchain:
        
        
            if block.hash != "" and block.hash != block.calulateBlockHash():
                return False
            else:
                for trans in block.transactions:
                    if trans.hashId != trans.computeHashId():
                        return False
            if block.id > 0 and block.hash != "":
                if lastblock != None and lastblock.hash != block.previousHashId:
                    return False
            lastblock = block
            
        return True    
    
    def hackBlockChain(self):
       
        hack = 0
    
        for block in self.blockchain.blockchain:
            for trans in block.transactions:
                for f in trans.fundToTransfers:
                    if hack == 0:
                        f = f+5
                        trans.fundToTransfers = [f]
                        hack += 1
        
    def faucet(self, wallet):
            #Genesisblock - previous hash id = 0
            genesisBlock = Block("0", 3, wallet)
            genesisBlock.id = 0
            
            #inputs for genesis blocks
            ut1 =  UTXo(wallet, wallet, 10001.0);
            ut2 =  UTXo(wallet, wallet, 12000.0);
            
            genesisTransaction =  Transaction(wallet, [wallet], [10000], [ut1, ut2]);
            b = genesisTransaction.prepareOutput()
            
            if(b):
                genesisTransaction.signTransaction(wallet.privateKey)
                self.addTransaction(genesisTransaction)
                #genesisBlock.mineBlock()
                #self.blockchain.addBlock(genesisBlock)
                
                wallet.setLocalLedger(self.blockchain)
                print("Balance : {0}" .format( wallet.getBalance()))    
                
        
    def transferFunds(self, sender, receivers, funds):
        return sender.transferFund(receivers, funds)    
        
        
    def getWalletByName(self, walletName):
        for wallet in self.connectedWallet.whiteListWallet:
            if wallet.name == walletName:
                return wallet
        
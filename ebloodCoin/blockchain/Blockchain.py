


class Blockchain(object):
     
    def __init__(self):
        self.blockchain = []
        
    def addBlock(self, block):
        self.blockchain.append(block)
 
    def getGenesisBlock(self):
        return self.blockchain[0]
    
    def getLastBlock(self):
        return self.blockchain[-1]
 
    def getSize(self):
        if self.blockchain == None:
            return 0
        else:
            return len(self.blockchain)
    
    def getBlock(self, i):
        return self.blockchain[i]
 
    def printBlockChain(self):
        print('')
        
    def findRelatedUTXos(self, all, spent, unspent, sentTransactions):
        for block in self.blockchain:
            for trans in block.transactions:
                print()
                
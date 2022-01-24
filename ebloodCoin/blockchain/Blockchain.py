from ebloodCoin.utils import StringUtils



class Blockchain(object):
     
    def __init__(self):
        self.blockchain = []
        
    def addBlock(self, block):
        self.blockchain.append(block)
 
    def getGenesisBlock(self):
        return self.blockchain[0]
    
    def getLastBlock(self):
        lastBlock =  self.blockchain[-1]
        return lastBlock
 
    def getSize(self):
        if self.blockchain == None:
            return 0
        else:
            return len(self.blockchain)
    
    def getBlock(self, i):
        return self.blockchain[i]
 
    def printBlockChain(self):
        print('')
        
    def display(self):
        for block in self.blockchain:
            for transIndex in range(len(block.transactions)):
                trans = block.transactions[transIndex]
                print(StringUtils.transString(trans))
        
    def findRelatedUTXos(self, publicKey):
       
        self.display()
       
       
        all = {}
        unspent = {}
        map = {}
       
        spent = []
        spending = 0.
        unspentTotal = 0.
        gain = 0.
        sentTransactions = []
        
        for block in self.blockchain:
            if len(block.transactions) >= 3:
                print()
            
            for transIndex in range(len(block.transactions)):
                trans = block.transactions[transIndex]
                if(transIndex > 0 and trans.sender.publicKey == publicKey):
                    sentTransactions.append(trans)
                    for input in trans.inputs:
                        spent.append(input)
                        spending += input.amount
                        map[input.hashId] = input
                        
                for output in trans.output:   
                    if output.receiver.publicKey == publicKey:
                        gain += output.amount
                        all[output.hashId] = output
                      
                      
        for hashId in all:   
            if(not hashId in map.keys()):
                unspent[hashId]=all.get(hashId)
                unspentTotal += unspent[hashId].amount
                      
                      
          
        return {'balance' : gain - spending,
                'unspent' : unspent,
                'unspentTotal' : unspentTotal,
                'all'   : all,
                'spent'   : spent,
                'sentTransactions' : sentTransactions
            }   
                             
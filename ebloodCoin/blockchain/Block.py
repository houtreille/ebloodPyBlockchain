
from time import time
from ebloodCoin.utils import HashingUtils, Parameters, SignatureUtils
import base64

class Block(object):


    MAX_TRANS_NB = 3

    def __init__(self, previousHashId, difficultyLevel = Parameters.MINING_DIFFICULTY, creator = None):
        self.previousHashId = previousHashId
        self.difficultyLevel = difficultyLevel
        self.creator = creator
        self.creatorSignature = None
        self.timestamp = time() * 1000
        self.transactions = []
        self.hash = ""
        self.nonce = 0
        self.id = None
    
        
    def calulateBlockHash(self):
        return HashingUtils.hash256(bytes(self.getBlockDataAsString(),'utf-8'),'hex')
    
    def getBlockDataAsString(self):
        
        sb = str(self.previousHashId) + str(self.timestamp)
        
        for trans in self.transactions :
            sb += str(trans.getHashId())
            
        sb += str(self.difficultyLevel)    
        sb += str(self.nonce)
        
        return sb
    
    def mineBlock(self):
        
        self.hash = self.calulateBlockHash()
        
        prefix = '0'*self.difficultyLevel
        
        while(not(self.hash.startswith(prefix))):
            self.nonce+=1
            self.hash = self.calulateBlockHash()
        
        return self.hash
    
    
    def signBlock(self):
        self.creatorSignature = base64.b64encode(SignatureUtils.sign(bytes(self.hash,'UTF-8'), self.creator.privateKey))
        
    def verifyBlock(self, key):    
        SignatureUtils.verify(bytes(self.hash,'UTF-8'), self.creator, key)
        
    def addTransaction(self, trans):
        self.transactions.append(trans)
        
    def getTotalTransactionSize(self):
        return len(self.transactions)
    
    def __str__(self, *args, **kwargs):
        return "Block#{0}".format(self.id)
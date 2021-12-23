'''
Created on 7 Dec 2021

@author: administration
'''
from time import time
from ebloodCoin.utils import HashingUtils, SignatureUtils
import base64

class Transaction(object):
    
    TRANSACTION_FEE  = 1.0
    sequentialNumberStatic = 0
    


    def __init__(self, sender, receivers, fundToTransfers, inputs):
        self.timeStamp = time()*1000
        self.sequentialNumber = Transaction.sequentialNumberStatic
        Transaction.sequentialNumberStatic+=1
        self.inputs = inputs
        self.output = []
        self.sender = sender
        self.receivers = receivers
        self.fundToTransfers = fundToTransfers
        self.hashId = self.computeHashId()
        self.signed = False
        
        
    def getTotalFundToTransfer(self):
        i = 0
        total = 0
        while i < len(self.fundToTransfers):   
            total+= self.fundToTransfers[i]
            i+=1
        
        return total
        
        
    def addOutputUTXo(self, utxo):
        if(not self.signed):
            self.output.append(utxo)
        
        
    def computeHashId(self):
         return HashingUtils.hash256(bytes(str(self) ,'UTF-8'))
            
        
    def getHashId(self):
        return self.hashId;
    
    def signTransaction(self, privateKey):
        self.creatorSignature = base64.b64encode(SignatureUtils.sign(bytes(self.hashId,'UTF-8'), privateKey))
        self.signed = True
        return self.creatorSignature
    
    
    def __str__(self):
     return self.transAsStr()
    
    def transAsStr(self):
        transData = str(self.timeStamp) +'_'+ str(self.sequentialNumber)
        
        for x in self.receivers:
            transData += str(x)
            
        for x in self.fundToTransfers:
            transData += str(x)
        
        return transData
       
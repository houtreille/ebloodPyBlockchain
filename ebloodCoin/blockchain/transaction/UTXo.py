'''
Created on 7 Dec 2021

@author: administration
'''
from time import time
from ebloodCoin.utils import HashingUtils

sequentialNumberStatic = 0

class UTXo(object):
    '''
    classdocs
    '''
    sequentialNumberStatic = 0


    def __init__(self, receiver, sender, amount):
        self.sequentialNumber = UTXo.sequentialNumberStatic
        UTXo.sequentialNumberStatic += 1
        self.receiver = receiver
        self.sender = sender
        self.amount = amount
        self.timestamp = time() * 1000
        self.hashId = self.computeHashId()
        
       
    def computeHashId(self):
        return HashingUtils.hash256(bytes(str(self),'UTF-8'), format='base64')  
    
    def __str__(self):
        return str(self.sequentialNumber) + str(self.receiver) + str(self.sender) + str(self.amount) + str(self.timestamp)
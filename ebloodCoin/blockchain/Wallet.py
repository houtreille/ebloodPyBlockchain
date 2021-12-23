'''
Created on 7 Dec 2021

@author: administration
'''
from ebloodCoin.utils import SignatureUtils
from Cryptodome.PublicKey import RSA

class Wallet(object):
    '''
    classdocs
    '''


    def __init__(self, name = None, initKey = True):
        if initKey:
            self.privateKey = SignatureUtils.newkeys(1024)
            self.publicKey = self.privateKey.publickey()
            self.password = name
        self.name = name
        
        
    def setName(self, name):
        self.name = name
        
    def setPassword(self, password):
        self.password = password
        
    def persistWallet(self):
        f = open(self.name + "_private.PEM",'wb')
        f.write(self.privateKey.export_key('PEM',passphrase=self.password))
        f.close()
        
    def retrieve(self, path, password):
        f = open(path,'r')
        
        print("Decrypting file " + path + " with " + password)
        
        self.privateKey = RSA.import_key(f.read(),passphrase=password)
        f.close()
        return self
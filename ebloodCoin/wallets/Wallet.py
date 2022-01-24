'''
Created on 7 Dec 2021

@author: administration
'''
from ebloodCoin.utils import SignatureUtils
from ebloodCoin.blockchain.transaction.Transaction import Transaction

class Wallet(object):
    '''
    classdocs
    '''


    def __init__(self, name = None, initKey = True, initWhiteList = True):
        
        
        if initKey:
            self.dict = SignatureUtils.newkeys(1024)
            self.privateKey = self.dict['privatekey']
            self.publicKey = self.dict['publickey']
        self.name = name
        self.assetHistory = {0 : 0.}
        self.whiteListWallet = []
        
        if initWhiteList:
            for i in [0,5]:
                self.whiteListWallet.append(Wallet("wallet" + str(i), True, False ))
            
    
    
    def transferFund(self, receivers, fundToTransfer):
        
        
        remainingFunds = self.localLedger.findRelatedUTXos(self.publicKey)
        available   = remainingFunds['unspentTotal']
        unspent     = remainingFunds['unspent']
        totalToTransfer = 0.;
        
        
        for amount in fundToTransfer:
            totalToTransfer = totalToTransfer + amount
        
        if available < totalToTransfer:
            raise NameError("Unsifficient funds {0} < {1}".format(available, totalToTransfer))
        
        #Prepare Inputs
        inputs = []
        available = 0;
        
        i = 0
        
        while (i < len(unspent) and available < totalToTransfer):
            ut = list(unspent.values())[i]
            available = ut.amount
            inputs.append(ut)
            i += 1
        
        transaction = Transaction(self, receivers, fundToTransfer, inputs)
    
        #Prepare Outputs
        b = transaction.prepareOutput()
        
        if b:
            transaction.signTransaction(self.privateKey);
            lastid = len(self.assetHistory)
            self.assetHistory[lastid] = self.getBalance()
            
            return transaction;
        else:
            return None;
        
        
        
    def setName(self, name):
        self.name = name
        
    def setPassword(self, password):
        self.password = password
        
    def setLocalLedger(self, ledger):
        self.localLedger = ledger
        
    def persistWallet(self):
        f = open(self.name + "_private.PEM",'wb')
        f.write(self.privateKey.export_key('PEM',passphrase=self.password))
        f.close()
        
    def retrieve(self, path, name, password):
        
        keys = SignatureUtils.importKeyFile(path + "\\" + name + "Private.PEM" , path + "\\" + name + "Public.PEM" , password)
        self.publicKey = keys['publicKey']
        self.privateKey = keys['privateKey']
        self.name = name
        self.password = password
        
        return self


    def getBalance(self):
        res = self.localLedger.findRelatedUTXos(self.publicKey)['balance']
        return res


    
    def getPrivateKeyAsStr(self):
        response = SignatureUtils.exportAsString(self.dict, 'PEM', None)
        
        return response['privateKeyB64']
    
    def getublicKeyAsStr(self):
        response = SignatureUtils.exportAsString(self.dict, 'PEM', None)
        
        return response['publicKeyB64']
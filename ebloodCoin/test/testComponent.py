'''
Created on 8 Dec 2021

@author: administration
'''
from ebloodCoin.blockchain.Block import Block
from ebloodCoin.blockchain.transaction.Transaction import Transaction
from ebloodCoin.utils import SignatureUtils, StringUtils
from ebloodCoin.blockchain.transaction.UTXo import UTXo
from ebloodCoin.test import testComponent
from ebloodCoin.wallets.Wallet import Wallet
from ebloodCoin.proxy.proxyController import proxyController



if __name__ == '__main__':
    
    print('XXX')
    testComponent.testRSA()
    



def testFaucet():
    
    popo = proxyController()
    wallet = Wallet(initKey=False)
    wallet.retrieve('''C:\Work\EclipseProjects\Python\pythonBlockchain\ebloodPyBlockchain\ebloodCoin''', 'eblood', "Reuss1r+")
    popo.connectedWallet = wallet
    popo.faucet(popo.connectedWallet)
    
    

def testRSA():
    
    passphrase = 'XYZ'
    portfolioName = 'eblood'
    
    dict = SignatureUtils.newkeys(1024)
    
     #PEMdictNoPW = SignatureUtils.exportKeys(dict, 'PEM', None)
     #DERdictNoPW = SignatureUtils.exportKeys(dict, 'DER', None)'''
    
     #'''PEMdictPW = SignatureUtils.exportKeys(dict, 'PEM', None)
      #DERdictPW = SignatureUtils.exportKeys(dict, 'DER', 'XXX')'''
    
    #'''strdictPW = SignatureUtils.exportAsString(dict, 'PEM', None)
    #strdictPW = SignatureUtils.exportAsString(dict, 'DER', 'XXX')'''
    
    SignatureUtils.exportAsFile(dict, 'PEM',  portfolioName+'Private.PEM', portfolioName+'public.PEM', passphrase)
    
    keys = SignatureUtils.importKeyFile(portfolioName+'Private.PEM', portfolioName+'public.PEM', passphrase)
    
    msg = "Amdoulilah"
    msgInBytes = bytes(msg,'UTF-8')
    
    signature = SignatureUtils.sign(msgInBytes, keys['privateKey'])
    
    verified = SignatureUtils.verify(msgInBytes, signature, keys['publicKey'])
    
    print(verified)
    
    
    
    

def testBlock():
    
    
    
    keys = SignatureUtils.newkeys(1024)
    publicKey = keys[0]
    privateKey = keys[1]
        
    block1 = Block(0, creator = privateKey)
    
    for x in range(6):
        trans = Transaction(str(x))
        block1.addTransaction(trans)
        
    block1.mineBlock()
    print('Block successfully mined, hashId:' + block1.hash)
    
    block1.signBlock()
    
    
    keys = SignatureUtils.newkeys(1024)    
    fakeKeys = SignatureUtils.newkeys(1024)    
    
    signature = SignatureUtils.sign(b"HELLO", keys[1])
    verifiedSignFake1 = SignatureUtils.verify(b"HELLO", signature, fakeKeys[0])
    verifiedSignFake2 = SignatureUtils.verify(b"HELLOX", signature, fakeKeys[0])
    verifiedSign      = SignatureUtils.verify(b"HELLO", signature, keys[0])
   
    print(verifiedSignFake1)
    print(verifiedSignFake2)
    print(verifiedSign)
    
    
    
def testTransaction():
    
    senderKeys = SignatureUtils.newkeys(1024)
    senderPublicKey = senderKeys[0]
    senderPrivateKey = senderKeys[1]
    
    StringUtils.getKeyString(senderPrivateKey)
    
    receiversKey = [SignatureUtils.newkeys(1024)[0], SignatureUtils.newkeys(1024)[0]]
    fundToTransfer = [100, 200]
    inputs = []
    
    uin = UTXo(senderPublicKey, senderPublicKey, 1000.)
    inputs.append(object)
    
    trans = Transaction(senderPublicKey, receiversKey,  fundToTransfer, inputs)
    trans.getTotalFundToTransfer()
    
    
    
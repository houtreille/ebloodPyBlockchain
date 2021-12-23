'''
Created on 8 Dec 2021

@author: administration
'''
from ebloodCoin.blockchain.Block import Block
from ebloodCoin.blockchain.transaction.Transaction import Transaction
from ebloodCoin.utils import SignatureUtils, StringUtils
from ebloodCoin.blockchain.transaction.UTXo import UTXo

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
    
    
    
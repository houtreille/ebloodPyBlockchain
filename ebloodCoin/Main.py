'''
Created on 6 Dec 2021

@author: administration
'''
from ebloodCoin.proxy.proxyController import proxyController
from ebloodCoin.wsgi import app
from ast import main


p = proxyController()

if __name__ == '__main__':    

        wallet = p.retrieveWallet(app.root_path, 'eblood', 'Reuss1r+')
        p.connectedWallet = wallet
       # p.faucet(wallet)
        receivers = p.getWalletByName("wallet0")
        #[wallet.whiteListWallet[0]]
    
        print(wallet.getBalance())
    
        t1 = p.transferFunds(wallet, [receivers], [8000.])
        p.addTransaction(t1)
        print(wallet.getBalance())
        
        t2 = p.transferFunds(wallet, [receivers], [2000.])
        p.addTransaction(t2)
        print(wallet.getBalance())
        
        t3 = p.transferFunds(wallet, [receivers], [3000.])
        p.addTransaction(t3)
        print(wallet.getBalance())
        
        t4 = p.transferFunds(wallet, [receivers], [2000.])
        p.addTransaction(t4)
        print(wallet.getBalance())
        
        t5 = p.transferFunds(wallet, [receivers], [500.])
        p.addTransaction(t5)
        print(wallet.getBalance())
        
        t6 = p.transferFunds(wallet, [receivers], [1000.])
        p.addTransaction(t6)
        print(wallet.getBalance())
        
        t7 = p.transferFunds(wallet, [receivers], [800.])
        p.addTransaction(t7)
        print(wallet.getBalance())
        
        blockchainVerified = p.verifyBlockChain()
    
    
        hack = 0
    
        for block in p.blockchain.blockchain:
            for trans in block.transactions:
                for f in trans.fundToTransfers:
                    if hack == 0:
                        f = f+5
                        trans.fundToTransfers = [f]
                        hack += 1
    
    
        blockchainVerified = p.verifyBlockChain()
    
    
        keyList = []
        valueList = []
        for key, value in wallet.assetHistory.items():
            keyList.append(key)
            valueList.append(value)
            
        print(keyList)
        print(valueList)
    
    
def hello():
    print('hello')
   
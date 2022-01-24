import base64

def getKeyString(key):
    keyStr = base64.b64encode(key)
    return keyStr

def transString(transaction):
    return "Trans#{0} = {1}->{2} [{3}]  hashID:{4}".format(transaction.sequentialNumber, transaction.sender.name, transaction.receivers[0].name, transaction.fundToTransfers[0], transaction.hashId)
    
    
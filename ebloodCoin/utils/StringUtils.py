import base64

def getKeyString(key):
    keyStr = base64.b64encode(key)
    return keyStr
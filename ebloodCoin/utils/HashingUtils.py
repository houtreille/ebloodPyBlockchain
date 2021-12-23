import hashlib
import base64

def hash256(objectToHash, format='hex'):
    
     
    m = hashlib.sha256()
    m.update(objectToHash)
    hash = m.digest()  
    
    if format == 'hex':  
        return hash.hex()
    elif format == 'bytes':  
        return hash
    elif format == 'base64':  
        return base64.b64encode(hash)
    else :
        return ''
    
def test():
   
    '''strToHash = "If you are a drop of tears in my eyes"'''
    hash = hash256(bytes(input(), 'UTF-8'))
    
    print(hash)
from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import *
from Cryptodome.Hash import SHA
from encodings.base64_codec import base64_encode
import base64
import binascii



def newkeys(keysize):
   random_generator = Random.new().read
   
   privateKey = RSA.generate(keysize, random_generator)
   publicKey = privateKey.publickey()
   
   response = {  # Dictionary
        'privatekey' : privateKey,
        'publickey'  : publicKey                                      
    }
   
   
   return response



def exportKeys(dictKeys, format, passphrase = None):
    
    privateKey = dictKeys['privatekey']
    publicKey =  dictKeys['publickey']

   
    privateKey = privateKey.exportKey(format, passphrase)
    publicKey =  publicKey.exportKey(format, passphrase)
    
    response = {  # Dictionary
    'exportedPrivateKey' : privateKey,
    'exportedPublicKey'  : publicKey                                      
    }
    
    return response
    
        
def exportAsString(dictKeys, format, passphrase = None):
    
    privateKey = dictKeys['privatekey']
    publicKey =  dictKeys['publickey']
    
    privateKeyPEM = privateKey.exportKey(format, passphrase)
    publicKeyPEM =  publicKey.exportKey(format, passphrase)
    
    base64privateKey = base64.b64encode(privateKeyPEM)
    base64publicKey = base64.b64encode(publicKeyPEM)

    hexprivateKey = binascii.hexlify(privateKeyPEM).decode('ascii')
    hexpublicKey = binascii.hexlify(publicKeyPEM).decode('ascii')

    response = {  # Dictionary
        'privateKeyB64': base64privateKey,
        'publicKeyB64': base64publicKey,
        'privateKeyHex' : hexprivateKey,
        'publicKeyHex'  : hexpublicKey                                      
    }

    return response


def exportAsFile(dictKeys, format, prv_filePath, pub_filePath, passphrase = None):
    
    dictExported = exportKeys(dictKeys, format, passphrase)
    
    fPRV = open(prv_filePath, 'wb')
    fPRV.write(dictExported['exportedPrivateKey'])
    fPRV.close()
    
    
    fpUB = open(pub_filePath, 'wb')
    fpUB.write(dictExported['exportedPublicKey'])
    fpUB.close()
        
        
        
def importKeyFile(prv_filePath, pub_filePath, passphrase = None):
    
    fpUB = open(pub_filePath, 'rb')
    publicKey = RSA.importKey(fpUB.read(), passphrase)
    
    fPRV = open(prv_filePath, 'rb')
    privateKey = RSA.importKey(fPRV.read(), passphrase)
    
    response = {  # Dictionary
        'publicKey': publicKey,
        'privateKey': privateKey                                     
    }

    return response
    
    
    
def getKeyString(key):
    return base64.b64encode(key)

def sign(message, priv_key, hashAlg = "SHA-256"):
   global hash
   hash = hashAlg
   signer = PKCS1_v1_5.new(priv_key)
   
   if (hash == "SHA-512"):
      digest = SHA512.new()
   elif (hash == "SHA-384"):
      digest = SHA384.new()
   elif (hash == "SHA-256"):
      digest = SHA256.new()
   elif (hash == "SHA-1"):
      digest = SHA.new()
   else:
      digest = MD5.new()
   digest.update(message)
   return signer.sign(digest)


def verify(message, signature, pub_key):
   signer = PKCS1_v1_5.new(pub_key)
   if (hash == "SHA-512"):
      digest = SHA512.new()
   elif (hash == "SHA-384"):
      digest = SHA384.new()
   elif (hash == "SHA-256"):
      digest = SHA256.new()
   elif (hash == "SHA-1"):
      digest = SHA.new()
   else:
      digest = MD5.new()
   digest.update(message)
   return signer.verify(digest, signature)
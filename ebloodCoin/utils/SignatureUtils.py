from Cryptodome import Random
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import *
from Cryptodome.Hash import SHA
from encodings.base64_codec import base64_encode
import base64



def newkeys(keysize):
   random_generator = Random.new().read
   key = RSA.generate(keysize, random_generator)
   return key


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
import hashlib
import sys
import binascii
import random

from Crypto.Cipher import AES
from Crypto import Random

msg = "test"

def encrypt(word, key, mode):
    plaintext = pad(word)
    encobj = AES.new(key, mode)
    return encobj.encrypt(plaintext)

def decrypt(ciphertext, key, mode):
    encobj = AES.new(key, mode)
    rtn = encobj.decrypt(ciphertext)
    return rtn

def pad(s):
    block_size = 16
    padding_size = block_size - (len(s) % block_size)
    padded_s = s + bytes([padding_size]) * padding_size
    return padded_s

rnd = random.randint(1, 2**128)

# Generate 256-bit session keys
keyA = hashlib.sha256(str(rnd).encode()).digest()
rnd = random.randint(1, 2**128)
keyB = hashlib.sha256(str(rnd).encode()).digest()

print('Long-term Key Alice =', binascii.hexlify(keyA))
print('Long-term Key Bob =', binascii.hexlify(keyB))

rnd = random.randint(1, 2**128)
keySession = hashlib.sha256(str(rnd).encode()).digest()

ya = encrypt(keySession, keyA, AES.MODE_ECB)
yb = encrypt(keySession, keyB, AES.MODE_ECB)

print("Encrypted key sent to Alice:", binascii.hexlify(ya))
print("Encrypted key sent to Bob:", binascii.hexlify(yb))

decipherA = decrypt(ya, keyA, AES.MODE_ECB)
decipherB = decrypt(yb, keyB, AES.MODE_ECB)

print("Session key:", binascii.hexlify(decipherA))
print("Session key:", binascii.hexlify(decipherB))

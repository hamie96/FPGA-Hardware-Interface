import time
import struct
import json
import sys
import requests
import bitcoin
import requests
from json_with_dates import loads

class Block:
    def __init__(self, block_hash, version, prev_block_hash, merkle_root, time, bits, nonce):
        self.block_hash = block_hash
        self.version = version
        self.prev_block_hash = prev_block_hash
        self.merkle_root = merkle_root
        self.time = time
        self.nonce = 0
        self.bits = bits
    
    def getBlockHash(self):
        return self.block_hash
    
    def getVersion(self):
        return self.version

    def getPrevBlockHash(self):
        return self.prev_block_hash

    def getMerkleRoot(self):
        return self.merkle_root

    def getTime(self):
        return self.time

    def getBits(self):
        return self.bits
    
    def setNonce(self, nonce):
        self.nonce = nonce

    def getNonce(self):
        return self.nonce

    def printBlock(self):
        return [self.block_hash, self.version, self.prev_block_hash, self.merkle_root, self.time, self.bits, self.nonce]

    def getFullhash(self):
        return struct.pack('<i', self.version).hex() + self.prev_block_hash + self.merkle_root + struct.pack('<i', self.time).hex() + self.bits + struct.pack('<i', self.nonce).hex()

 
class User:
    
    def __init__(self, name):
        self.name = name
        self.private_key = None

    def setPrivateKey(self, private_key):
        self.private_key = private_key

    def createPrivateKey(self):
        self.private_key = bitcoin.random_key()

    def createPublicKey(self, private_key):
        self.public_key = bitcoin.privtopub(private_key)

    def createBitcoinAddress(self, public_key):
        self.bitcoin_addr = bitcoin.pubtoaddr(public_key)
   
    def getBitcoinAddress(self):
        return self.bitcoin_addr

    def returnUser(self):
        return ("User:" + self.name + "\nPrivate Key:" + str(self.private_key))
    
    def getPrivateKey(self):
        return self.private_key
    
    def getPublicKey(self):
        return self.public_key
   
    def getBalance(self):
        try:
            balance_request = requests.get('https://blockexplorer.com/api/addr/{}'.format(self.bitcoin_addr))
            balance = loads(balance_request.text)
        except:
            return "Could not get balance"
        return(balance['balance'])

    def getBalanceRequest(self):
         balance_request = requests.get('https://blockexplorer.com/api/addr/{}'.format(self.bitcoin_addr))
         return balance_request.text

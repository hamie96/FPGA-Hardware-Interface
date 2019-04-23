import requests
from json_with_dates import loads
from network_interface import *


user1 = User('Charles')
user1.createPrivateKey()
user1.createPublicKey(user1.getPrivateKey())
user1.createBitcoinAddress(user1.getPublicKey())
print(user1.returnUser())
print('')
print('')
print(user1.getBalance())

block_request = requests.get('https://blockexplorer.com/api/block/0000000000000000079c58e8b5bce4217f7515a74b170049398ed9b8428beb4a')
print('')
print(type(block_request))
print(user1.getBalanceRequest())

block = loads(block_request.text)

block1 = Block(block['hash'],block['version'],block['previousblockhash'],block['merkleroot'],block['time'],block['bits'], block['nonce'])

print(block1.printBlock())
print(block1.getFullhash() )
print('')

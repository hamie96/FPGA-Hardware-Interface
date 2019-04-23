# FPGA Blockchain Miner
This is an implementation of a blockchain miner for a FPGA Board

## Network Interface
The Network Interface interface utilizes the following python packages
```bash
pip3-install requests
pip3-install bitcoin
```

The Bitcoin API is utilized to create public keys, private keys, and bitcoin addresses

## Example
An example of the creation of a block is given in the example1.py file

### Example User Creation:
```python
user1 = User('Charles')
user1.createPrivateKey()
print(user1.returnUser())
```

All Blocks are pulled from the [Blockexplorer website](https://blockexplorer.com/)

### Example Block Creation:
```python
block_request = requests.get('https://blockexplorer.com/api/block/0000000000000000079c58e8b5bce4217f7515a74b170049398ed9b8428beb4a')

block = loads(block_request.text)

block1 = Block(block['hash'],block['version'],block['previousblockhash'],block['merkleroot'],block['time'],block['bits'], block['nonce'])
```

## Contributors
| Name | Module |
| ----- | ----- |
| Greggor | Mining Hardware |
| Oliver | Hardware Interface |
| Hamilton | Networking Interface|
| Kirsty | Monitoring Interface |

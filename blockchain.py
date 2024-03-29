from functools import reduce
import hashlib as hl

import json
import pickle

# Import two functions from our hash_util.py file. Omit the ".py" in the import
from hash_util import hash_block
from block import Block
from imagetransaction import ImageTransaction
from verification import Verification


class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions

        self.__open_image_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
        self.__peer_nodes=set()

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter 
    def chain(self, val):
        self.__chain = val


    def get_open_transactions(self):
        return self.__open_image_transactions[:]

    def load_data(self):
        """Initialize blockchain + open transactions data from a file."""
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [ImageTransaction(
                        tx['id'], tx['imagename'], tx['imagehash'],tx['proof']) for tx in block['image_transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                
                open_transactions = json.loads(file_content[1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = ImageTransaction(
                        tx['id'], tx['imagename'], tx['imagehash'],tx['proof'])
                    updated_transactions.append(updated_transaction)
                self.__open_image_transactions = updated_transactions
                
                peer_nodes=json.loads(file_content[1][:-1])
                self.__peer_nodes=set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup!')

    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index,block_el.previous_hash,[tx.__dict__ for tx in block_el.image_transactions],block_el.proof,block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_image_transactions]
                f.write(json.dumps(saveable_tx))

                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_image_transactions, last_hash, proof):
            proof += 1

        return proof

    
    
    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    # This function accepts two arguments.
    # One required one (transaction_amount) and one optional one (last_transaction)
    # The optional one is optional because it has a default value => [1]

    def add_image_transaction(self,id, imagename, imagehash, proof):
        
        transaction = ImageTransaction(id, imagename, imagehash, proof)
        
        self.__open_image_transactions.append(transaction)
        print(self.__open_image_transactions)

        self.save_data()
        return True
        
    def mine_block(self):
        """Create a new block and add open transactions to it."""
        # Fetch the currently last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value)
        hashed_block = hash_block(last_block)
        print (hashed_block)

        proof = self.proof_of_work()

       
        copied_transactions = self.__open_image_transactions[:]
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof=proof)
        self.__chain.append(block)
        
        print(self.__chain)
        self.__open_image_transactions = []
        self.save_data()
        return True


    def add_peer_node(self,node):
        '''Adds new node peer node set
        arguments: __peer_nodes
        '''
        self.___peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self,node):
        self.__peer.nodes.discard(node)
        self.save_data()
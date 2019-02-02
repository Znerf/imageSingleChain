from time import time

from printable import Printable

class Block(Printable):
    def __init__(self, index, previous_hash, image_transactions, proof, time=time()):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.image_transactions = image_transactions
        self.proof = proof



from blockchain import Blockchain 
import hashlib as hl
import json

from io import StringIO,BytesIO

import base64 
import PIL.Image

#from imagetohash import Image_to_hash
from verification import Verification
from imagetohash import Image_to_hash

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'MAX'
        self.blockchain=Blockchain(self.id)

    def get_image_name(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        image_name = input('Enter the image name :')

        return image_name

    def get_images(self,time ,time2):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        time = input('Enter time :')
        time2 = input('Enter time :')


        return time,time2


    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.chain:
            print('Outputting Block')
            print(block)
        else:
            print('-' * 20)

    def show_photo(self):
        for block in self.blockchain.chain:
            
            for a in block.image_transactions:
                
                with open(a.imagename, "rb") as f:
                    data = f.read()
                    data=base64.b64decode(data)
                    file_like = BytesIO(data)
                    img = PIL.Image.open(file_like)
                    img.show()
                


    def listen_for_input(self):
        waiting_for_input = True

        # A while loop for the user input interface
        # It's a loop that exits once waiting_for_input becomes False or when break is called
        while waiting_for_input:
            print('Please choose')
            print('1: Add a new image transaction ')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check photo')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                participants = self.get_image_name()
                
                # Add the transaction amount to the blockchain
                image=Image_to_hash(participants)
                image.photo_encode()
                hashed1=image.create_hash()# hl.sha256(json.dumps(participants).encode()).hexdigest()
                

                
                if self.blockchain.add_image_transaction( id=self.id,imagename=participants, imagehash=hashed1, proof=2 ):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
            elif user_choice=='2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                self.show_photo()

            elif user_choice=='q':
                waiting_for_input=False
                
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                # Break out of the loop
                break
            if not Verification.verify_transaction(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain2!')
                # Break out of the loop
                break
        else:
            print('User left!')

        print('Done!')

    

node = Node()
node.listen_for_input()
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from base64 import b64decode, b64encode


import PIL.Image
import hashlib as hl
import os

# assume data contains your decoded image


class Image_to_hash:
	def __init__(self, name):
		self.name=name
		
		

	def photo_encode(self):
		with open(self.name, "rb") as f:
			data = f.read()
			data=base64.b32encode(data)
			
		with open(self.name,"wb") as f:
			f.write(data)
			

		
	def open_photo(self):
		with open(self.name, "rb") as f:
			data = f.read()
			data=base64.b32decode(data)
			#data= data.decode("base64")
			file_like = StringIO(data)

			img = PIL.Image.open(file_like)
			img.show()
			

	def create_hash(self):
		with open(self.name, "rb") as f:
			data = f.read()
			return hl.sha256(data).hexdigest()

	'''
	def rename(self):
		os.rename(self.name,'pho/'+self.create_hash()+'.png')
		print self.name
		self.name='pho/'+self.create_hash()+'.png'
	'''

a=Image_to_hash("pho/1.png")
a.photo_encode()
a.open_photo()
b=a.create_hash()

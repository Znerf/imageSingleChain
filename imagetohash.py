
from io import StringIO,BytesIO

import base64 
import PIL.Image
import hashlib as hl
import json


# assume data contains your decoded image


class Image_to_hash:
	def __init__(self, name):
		self.name=name
		
	def photo_encode(self):
		with open(self.name, "rb") as imageFile:
			str = base64.b64encode(imageFile.read())
		with open(self.name,"wb") as f:
			f.write(str)
		
	def open_photo(self):
		with open(self.name, "rb") as f:
			data = f.read()
			data=base64.b64decode(data)
			file_like = BytesIO(data)
			img = PIL.Image.open(file_like)
			img.show()
			

	def create_hash(self):
		with open(self.name, "rb") as f:
			data = f.read()
			return hl.sha256((str(data)+self.name).encode()).hexdigest()

	


from collections import OrderedDict

from printable import Printable

class ImageTransaction(Printable):
    def __init__(self,id, imagename, imagehash,proof):
        self.id = id
        self.imagename = imagename
        self.imagehash = imagehash
        self.proof=proof

    def to_ordered_dict(self):
        return OrderedDict([('imagename', self.imagename), ('imagehash', self.imagehash)])

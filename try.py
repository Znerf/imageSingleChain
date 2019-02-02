from base64 import b64decode, b64encode

image_handle = open('pho//2.png', 'rb')

raw_image_data = image_handle.read()

encoded_data = b64encode(raw_image_data)
compressed_data = zlib.compress(encoded_image, 9) 

uncompressed_data = zlib.decompress(compressed_data)
decoded_data = b64decode(uncompressed_data)

new_image_handle = open('new_test_image.jpg', 'wb')

new_image_handle.write(decoded_data)
new_image_handle.close()
image_handle.close()
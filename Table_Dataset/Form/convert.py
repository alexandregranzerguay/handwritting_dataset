from PIL import Image
import glob
import os, sys

print('IT WORKS .......')
for name in glob.glob('./'+sys.argv[1]+'/*.tif'):
    im = Image.open(name)
    name = str(name).rstrip(".tif")
    im.save(name + '.jpg', 'JPEG')

from PIL import Image
import glob
import os

for name in glob.glob('*.tif'):
    im = Image.open(name)
    name = str(name).rstrip(".tif")
    im.save(name + '.jpg', 'JPEG')

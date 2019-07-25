from PIL import Image
import glob
import os

for name in glob.glob('*.tif'):
    if glob.glob(name +'.jpg'):
        continue
    im = Image.open(name)
    name = str(name).rstrip(".tif")
    im.save(name + '.jpg', 'JPEG')

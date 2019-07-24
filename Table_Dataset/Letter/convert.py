from PIL import Image
import glob
import os

for name in glob.glob('*.tif'):
    old_name = name
    im = Image.open(name)
    name = str(name).rstrip(".tif")
    im.save(name + '.jpg', 'JPEG')
    os.remove(old_name)
import imquality.brisque as brisque
import PIL.Image
import os
from os.path import expanduser
home = expanduser("~")



clear_dir = home+"/Downloads/QA-Polyp/train/0-clear/";

blur_dir = home+"/Downloads/QA-Polyp/train/1-blurry/"

clear_images = os.listdir(clear_dir)

blur_images  = os.listdir(blur_dir)

i=0

for image in clear_images:
    path = clear_dir+image

    img = PIL.Image.open(path)
    print(image+":"+str(brisque.score(img)))

    i=i+1

    if i >10:
        break

i=0
for image in blur_images:
    path = blur_dir+image

    img = PIL.Image.open(path)
    print(image+":"+str(brisque.score(img)))

    i=i+1

    if i >10:
        break




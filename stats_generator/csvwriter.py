import csv
import imquality.brisque as brisque
import PIL.Image
import os
from os.path import expanduser
home = expanduser("~")

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = ['im_names']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()

    clear_dir = home + "/Downloads/QA-Polyp/train/0-clear/";

    blur_dir = home + "/Downloads/QA-Polyp/train/1-blurry/"

    clear_images = os.listdir(clear_dir)

    blur_images = os.listdir(blur_dir)



    for image in clear_images:
        path = clear_dir + image

        img = PIL.Image.open(path)

        value = '0-clear/'+image

        writer.writerow({'im_names': value})


    #count -829 for clear
    #233 blur


    for image in blur_images:
        path = blur_dir + image

        img = PIL.Image.open(path)


        value = '1-blurry/' + image

        writer.writerow({'im_names':value})



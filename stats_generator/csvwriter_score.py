import csv
import imquality.brisque as brisque
import PIL.Image
import os
from os.path import expanduser
home = expanduser("~")

with open('scores.csv', 'w', newline='') as csvfile:
    fieldnames = ['scores']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()

    clear_dir = home + "/Downloads/QA-Polyp/train/0-clear/";

    blur_dir = home + "/Downloads/QA-Polyp/train/1-blurry/"

    clear_images = os.listdir(clear_dir)

    blur_images = os.listdir(blur_dir)


    i=1

    for image in clear_images:
        path = clear_dir + image

        img = PIL.Image.open(path)

        value = (brisque.score(img))/4



        writer.writerow({'scores': value})

        print(str(i)+":"+str(value))
        i =i+1


    #count -829 for clear
    #233 blur


    for image in blur_images:
        path = blur_dir + image

        img = PIL.Image.open(path)

        value = brisque.score(img)*(1.5)

        writer.writerow({'scores':value})

        print(str(i) + ":" + str(value))
        i = i + 1
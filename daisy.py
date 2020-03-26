from skimage.feature import daisy
from skimage import data
import matplotlib.pyplot as plt
import csv
import imquality.brisque as brisque
import PIL.Image
import os
from os.path import expanduser
import numpy as np
import sys
from skimage.transform import rescale, resize, downscale_local_mean


def daisyFeatures(img_path):


    img = PIL.Image.open(img_path).convert('L')

    # (width, height) = (img.width / 2, img.height / 2)

    # img = img.resize((int(width), int(height)))

    descs, descs_img = daisy(img, step=180, radius=58, rings=2, histograms=6,
                         orientations=8, visualize=True)

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.imshow(descs_img)
    descs_num = descs.shape[0] * descs.shape[1]
    ax.set_title('%i DAISY descriptors extracted:' % descs_num)
    print("DAISY descriptors extracted : " + img_path + " : " + str(descs_num))
    plt.show()




home = expanduser("~")

clear_dir = home + "/Downloads/QA-Polyp/train/0-clear/";

blur_dir = home + "/Downloads/QA-Polyp/train/1-blurry/"

clear_images = os.listdir(clear_dir)

blur_images = os.listdir(blur_dir)


LOOP = 4

for i in range(LOOP):

    try:

        path = clear_dir+clear_images[i]
        daisyFeatures(path)

        path = blur_dir+blur_images[i]
        daisyFeatures(path)
    except:
        print("error occurred :", sys.exc_info()[1])







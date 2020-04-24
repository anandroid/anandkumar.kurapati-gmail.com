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

from blob_detection import blobdetection
from orb import  orb




home = expanduser("~")

clear_dir = home + "/Downloads/QA-Polyp/train/0-clear/";

blur_dir = home + "/Downloads/QA-Polyp/train/1-blurry/"

clear_images = os.listdir(clear_dir)

blur_images = os.listdir(blur_dir)


LOOP = 4

for i in range(LOOP):

    try:

        path = clear_dir+clear_images[i]
        #print(path+" Features :"+str(blobdetection(path)))
        print(path+" Features :"+str(orb(path)))


        path = blur_dir+blur_images[i]
        #print(path + " Features :" + str(blobdetection(path)))
        print(path+" Features :"+str(orb(path)))

    except:
        print("error occurred :", sys.exc_info()[1])







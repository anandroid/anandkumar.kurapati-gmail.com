from PIL import Image
import numpy
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



polyp_dir = home + "/Downloads/TrainingSet_NewGT/ShortVD_wp_2/GT/";

polyp_images = os.listdir(polyp_dir)

LOOP = 4

for i in range(LOOP):
    path = polyp_dir + polyp_images[i]
    im = Image.open(path)
    imarray = numpy.array(im)
    imarray.shape
    #im.show()
    plt.imshow(im, cmap='gray')
    plt.axis('off')
    plt.show()

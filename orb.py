from skimage import data
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image



def orb(img_path):
    image = PIL.Image.open(img_path).convert('L')
    img1 = np.array(image)
    img2 = tf.rotate(img1, 180)

    descriptor_extractor = ORB(n_keypoints=200)

    descriptor_extractor.detect_and_extract(img1)
    keypoints1 = descriptor_extractor.keypoints
    descriptors1 = descriptor_extractor.descriptors

    descriptor_extractor.detect_and_extract(img2)
    keypoints2 = descriptor_extractor.keypoints
    descriptors2 = descriptor_extractor.descriptors

    matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)






    fig, ax = plt.subplots(nrows=2, ncols=1)

    plt.gray()

    plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
    ax[0].axis('off')
    ax[0].set_title(img_path)


    plt.show()

    return matches12.shape[0]



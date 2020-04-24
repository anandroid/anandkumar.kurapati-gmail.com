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
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score

from blob_detection import blobdetection
from orb import  orb

def SVM(clear_scores1,clear_scores2,blur_scores1,blur_scores2,):
    SVM_TRAIN_RATIO = 0.6

    X, y = [], []

    for i in range(int(len(clear_scores1) * SVM_TRAIN_RATIO)):
        X.append([clear_scores1[i], clear_scores2[i]])
        y.append(0)

    for i in range(int(len(blur_scores1) * SVM_TRAIN_RATIO)):
        X.append([blur_scores1[i], blur_scores2[i]])
        y.append(1)

    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(X, y)

    Y_true = []
    Y_pred = []

    misPredicts = 0
    for i in range(int(len(clear_scores1) * SVM_TRAIN_RATIO), len(clear_scores1)):
        x = [[clear_scores1[i], clear_scores2[i]]]
        y = clf.predict(x)
        Y_true.append(0)
        Y_pred.append(y)
        true_value = "Clear "
        pred_value = "Clear"
        if y[0] == 1:
            pred_value = "Blurry"
            misPredicts = misPredicts + 1

        print("Clear | score :" + str(x) + pred_value)

    for i in range(int(len(blur_scores1) * SVM_TRAIN_RATIO), len(blur_scores1)):
        x = [[blur_scores1[i], blur_scores2[i]]]
        y = clf.predict(x)
        Y_true.append(1)
        Y_pred.append(y)
        true_value = "Blurry "
        pred_value = "Blurry"
        if y[0] == 0:
            pred_value = "Clear"
            misPredicts = misPredicts + 1

        print("Blurry | score :" + str(x) + pred_value)

    total = (len(blur_scores1) - int(len(blur_scores1) * SVM_TRAIN_RATIO)) + \
            (len(clear_scores1) - int(len(clear_scores1) * SVM_TRAIN_RATIO))

    print("Total :" + str(total) + " Mispredicted :" +
          str(misPredicts))

    print("Accuracy :" + str(accuracy_score(Y_true, Y_pred)))
    print("ROC :"+roc_auc_score(Y_true, Y_pred))







home = expanduser("~")

clear_dir = home + "/Downloads/QA-Polyp/train/0-clear/";

blur_dir = home + "/Downloads/QA-Polyp/train/1-blurry/"

clear_images = os.listdir(clear_dir)

blur_images = os.listdir(blur_dir)




clear_orb_scores = []
clear_blob_scores = []
dummy_clear_scores=[]

for image in clear_images:
    path = clear_dir + image

    clear_orb_scores.append(orb(path))
    #clear_blob_scores.append(blobdetection(path))
    dummy_clear_scores.append(0)


print("################")


blur_orb_scores = []
blur_blob_scores = []
dummy_blur_scores=[]
for image in blur_images:
    path = blur_dir + image

    blur_orb_scores.append(orb(path))
    #blur_blob_scores.append(blobdetection(path))
    dummy_blur_scores.append(0)

print("SVM ORB")
print(clear_orb_scores,dummy_clear_scores,blur_orb_scores,dummy_blur_scores)

print("SVM BLOB")
#print(clear_blob_scores,dummy_clear_scores,blur_blob_scores,dummy_blur_scores)

print("SVM ORB , BLOB")
#print(clear_blob_scores,clear_orb_scores,blur_blob_scores,blur_orb_scores)





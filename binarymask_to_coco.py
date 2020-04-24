import json
import numpy as np
from pycocotools import mask
from skimage import measure


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
from PIL import Image
import torch

from pycococreatortools import  *

from skimage.transform import rescale, resize, downscale_local_mean

from blob_detection import blobdetection
from orb import  orb




home = expanduser("~")


dir = home + "/Downloads/TrainingSet_NewGT/shortVD_wp_4/GTJPG/";

images = os.listdir(dir)
json_str=""

mainjson = {
        "images":[],
        "categories": [],
        "annotations":[]
    }


img_id =0

VALID_IMAGE_START=84
valid_image_index=1;

loop_id=0

for index in range(int(len(images)*0.75)):

    image = images[index]

    if len(image.split("_"))<5:
        print("bad one "+image)
        continue


    image_frame_id = (int)(image.split("_")[4])
    image_format  = image.split(".")[1]

    if image_frame_id<VALID_IMAGE_START:
        continue

    im = Image.open(dir+image)
    np_im = np.array(im,dtype=np.uint8)

    #img_id = image.split("_")[4]


    image_name = image
    image_name = image_name.replace("tiff","jpg")
    image_name = image_name.replace("GT","RGB")

    image_json = {
        "height": np_im.shape[0],
        "width":np_im.shape[1],
        "id": img_id,
        "file_name":image_name
    }

    mainjson["images"].append(image_json)




    ground_truth_binary_mask = np_im


    fortran_ground_truth_binary_mask = np.asfortranarray(ground_truth_binary_mask)
    encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
    ground_truth_area = mask.area(encoded_ground_truth)
    ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
    contours = measure.find_contours(ground_truth_binary_mask, 0.5)

    maskbits = im
    maskbits = np.array(maskbits)
    #mask = resize(mask, (768, 1024), preserve_range=True)
    maskbits = maskbits.astype(np.uint8)
    maskbits[maskbits < 255] = 0
    maskbits[maskbits == 255] = 1
    obj_ids = np.unique(maskbits)
    obj_ids = obj_ids[1:]
    masks = maskbits == obj_ids[:, None, None]
    num_objs = len(obj_ids)

    boxes = []
    for i in range(num_objs):
        pos = np.where(masks[i])
        xmin = int(np.min(pos[1]))
        xmax = int(np.max(pos[1]))
        ymin = int(np.min(pos[0]))
        ymax = int(np.max(pos[0]))
        boxes.append([xmin, ymin, xmax, ymax])

    boxestensor = torch.as_tensor(boxes, dtype=torch.float32)

    area = (boxestensor[:, 3] - boxestensor[:, 1]) * (boxestensor[:, 2] - boxestensor[:, 0])

    annotation = {
        "segmentation": [],
        "area": area.tolist()[0],
        "iscrowd": 0,
        "image_id": img_id,
        "bbox": boxes[0],
        "category_id": 1,
        "id": 1,
        "height": np_im.shape[0],
        "width": np_im.shape[1],
    }



    for contour in contours:
        contour = np.flip(contour, axis=1)
        segmentation = contour.ravel().tolist()
        annotation["segmentation"].append(segmentation)

    annotation["id"] = img_id
    loop_id = loop_id + 1
    mainjson["annotations"].append(annotation)

    ''' 
    segmentations = binary_mask_to_polygon(ground_truth_binary_mask,2)

    for segmentation in segmentations:
        annotation = {
            "segmentation": [],
            "area": ground_truth_area.tolist(),
            "iscrowd": 0,
            "image_id": img_id,
            "bbox": ground_truth_bounding_box.tolist(),
            "category_id": 1,
            "id": 1
        }

        annotation["segmentation"].append(segmentation)
        annotation["id"] = loop_id
        loop_id = loop_id + 1
        mainjson["annotations"].append(annotation)
     '''

    #json_str = json_str+"\n"+json.dumps(annotation, indent=4)
    print(image)

    img_id = img_id+1


category_json = {
            "supercategory": "lesion",
            "id": 1,
            "name": "polyp"
        }

mainjson["categories"].append(category_json)


#print("formed json")

with open('train_annotations_multiple_segmentations_75_wp.json', 'w', newline='') as file:
    file.write(json.dumps(mainjson, indent=4))
    file.close()

print("done")
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
from shapely.geometry import Polygon, MultiPolygon

from skimage.transform import rescale, resize, downscale_local_mean

from blob_detection import blobdetection
from orb import  orb


from PIL import Image # (pip install Pillow)

def create_sub_masks(mask_image):
    width, height = mask_image.size

    # Initialize a dictionary of sub-masks indexed by RGB colors
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            pixel = mask_image.getpixel((x,y))

            # If the pixel is not black...
            if pixel != 0:
                # Check to see if we've created a sub-mask...
                pixel_str = str(pixel)
                sub_mask = sub_masks.get(pixel_str)
                if sub_mask is None:
                   # Create a sub-mask (one bit per pixel) and add to the dictionary
                    # Note: we add 1 pixel of padding in each direction
                    # because the contours module doesn't handle cases
                    # where pixels bleed to the edge of the image
                    sub_masks[pixel_str] = Image.new('1', (width+2, height+2))

                # Set the pixel value to 1 (default is 0), accounting for padding
                sub_masks[pixel_str].putpixel((x+1, y+1), 1)

    return sub_masks

def create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd):
    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)
    contours = measure.find_contours(sub_mask, 0.5, positive_orientation='low')

    segmentations = []
    polygons = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(0.2, preserve_topology=False)
        polygons.append(poly)
        segmentation = np.array(poly.exterior.coords).ravel().tolist()
        segmentations.append(segmentation)

    # Combine the polygons to calculate the bounding box and area
    multi_poly = MultiPolygon(polygons)
    x, y, max_x, max_y = multi_poly.bounds
    width = max_x - x
    height = max_y - y
    bbox = (x, y, width, height)
    area = multi_poly.area

    annotation = {
        'segmentation': segmentations,
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': bbox,
        'area': area
    }

    return annotation





home = expanduser("~")


dir = home + "/Downloads/TrainingSet_NewGT/shortVD_wp_4/GT/";

images = os.listdir(dir)
json_str=""

mainjson = {
        "images":[],
        "categories": [],
        "annotations":[]
    }


is_crowd=0

annotations = []

img_id =0

VALID_IMAGE_START=84
valid_image_index=1;

loop_id=0

for image in images:

    if len(image.split("_"))<5:
        print("bad one "+image)
        continue


    image_frame_id = (int)(image.split("_")[4])
    image_format  = image.split(".")[1]

    if image_frame_id<VALID_IMAGE_START:
        continue

    im = Image.open(dir+images[0])
    np_im = np.array(im)

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

    sub_masks = create_sub_masks(im)
    for color, sub_mask in sub_masks.items():
        category_id = 1
        annotation = create_sub_mask_annotation(sub_mask, img_id, category_id, loop_id, is_crowd)
        annotations.append(annotation)
        loop_id += 1






    img_id = img_id+1


category_json = {
            "supercategory": "lesion",
            "id": 1,
            "name": "polyp"
        }

mainjson["categories"].append(category_json)

mainjson["annotations"] = annotations


print("formed json")

with open('train_annotations_advanced.json', 'w', newline='') as file:
    file.write(json.dumps(mainjson, indent=4))
    file.close()

print("done")
import csv
import imquality.brisque as brisque
import PIL.Image
import os
from os.path import expanduser
home = expanduser("~")

with open('refids.csv', 'w', newline='') as csvfile:
    fieldnames = ['ref_ids']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()

    for i in range(1062):

      writer.writerow({'ref_ids': i+1})






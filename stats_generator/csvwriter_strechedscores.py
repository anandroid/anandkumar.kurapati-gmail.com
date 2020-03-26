import csv
import imquality.brisque as brisque
import PIL.Image
import os
from os.path import expanduser
home = expanduser("~")


scoresList=[]

with open('oldscores.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        score = float(row['scores'])
        if score > 30:
            score = score * 1.5
        scoresList.append(score)

with open('freshscores.csv', 'w', newline='') as csvfile:
      fieldnames = ['scores']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      for score in scoresList:
          score = score*1.5
          writer.writerow({'scores':score})


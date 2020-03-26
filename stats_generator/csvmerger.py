import csv

namesList = []

with open('names.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
           name = row['im_names']
           namesList.append(name)


scoresList = []

with open('scores.csv', newline='') as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
           score = float(row['scores'])
           scoresList.append(score)


newnamesList = []
newscoresList= []


middleIndex = 830


i=0
basei=0

while i < len(namesList):
    if middleIndex + basei >= len(namesList):
       break

    i=basei
    newnamesList.append(namesList[i])
    newscoresList.append(scoresList[i])
    i=i+1
    newnamesList.append(namesList[i])
    newscoresList.append(scoresList[i])
    i=middleIndex+basei
    newnamesList.append(namesList[i])
    newscoresList.append(scoresList[i])

    basei = basei+2

blurryDuplicates=500
blurryIndex=0
while basei < middleIndex:
    basei = basei+1
    newnamesList.append(namesList[basei])
    newscoresList.append(scoresList[basei])

    if (blurryIndex<blurryDuplicates and blurryIndex+middleIndex<len(namesList)):
        newnamesList.append(namesList[middleIndex+blurryIndex])
        newscoresList.append(scoresList[middleIndex+blurryIndex])

    blurryIndex=blurryIndex+1











with open('newnames.csv', 'w', newline='') as csvfile:
    fieldnames = ['im_names']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()

    for i in range(len(newnamesList)):

      writer.writerow({'im_names': newnamesList[i]})

with open('newscores.csv', 'w', newline='') as csvfile:
    fieldnames = ['scores']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()

    for i in range(len(newscoresList)):

      writer.writerow({'scores': newscoresList[i]})

with open('newrefids.csv', 'w', newline='') as csvfile:
    fieldnames = ['ref_ids']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


    writer.writeheader()

    for i in range(len(newscoresList)):

      writer.writerow({'ref_ids': i+1})

import csv
import json

files = open("input/csv/artworks/a/a0001.txt")
csvfile = open('artworksjson.csv', mode='w')
art_writer = csv.writer(csvfile, delimiter=',')
art_writer.writerow(['accession','title', 'medium', 'movement', 'era', 'subject', 'date'])
csvfile2 = open('subjects.csv', mode='w')
subject_writer = csv.writer(csvfile2, delimiter=',')
subjectlist = []


for each in files:
	file = "input/csv/artworks/a/" + each.strip()
	data = open(file).read()
	try:
		data2 = json.loads(data)
	except:
		continue
	#print(data2.keys())
	#(['acno', 'acquisitionYear', 'all_artists', 'catalogueGroup', 'classification', 'contributorCount', 'contributors', 'creditLine', 'dateRange', 
	#	'dateText', 'depth', 'dimensions', 'foreignTitle', 'groupTitle', 'height', 'id', 'inscription', 'medium', 'movementCount', 'movements', 'subjectCount', 
	#	'subjects', 'thumbnailCopyright', 'thumbnailUrl', 'title', 'units', 'url', 'width'])
	try:
		movements = data2['movements']
		movement = movements[-1]['name'].replace('\r', "")
		movement = movement.replace("\n", "")
		#print("MOVEMENT = " + movement)
		era = movements[0]['era']['name']
		era = era.replace('\r', "")
		era = era.replace('\n', "")
	except:
		movement = ""
		era = ""
	
	try:
		subjects = []
		subject = data2['subjects']
		#print(subject['children'])
		for each in subject['children']:
			#print(each['children'])
			for item in each['children']:
				for sub in item['children']:
					subjects.append(sub['name'])
					if sub['name'] not in subjectlist:
						subjectlist.append(sub['name'].replace(",", "").strip())
	except:
		subjects = []

	medium = data2['medium'].replace("\r", "")
	medium = medium.replace("\n", "")

	date = data2['dateText'].replace("\r", "")
	date = date.replace("\n", "")

	art_writer.writerow([data2['acno'],data2['title'], medium, movement, era, subjects, date])
	#print(data2['title'], data2['medium'], movement, era, subjects, data2['dateText']
subject = []
for each in subjectlist:
	if each not in subject:
		subject.append(each.replace(",","").strip())
for each in subject:
	subject_writer.writerow([each])

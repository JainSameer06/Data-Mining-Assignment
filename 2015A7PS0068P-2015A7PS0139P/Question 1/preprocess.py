import csv
from collections import defaultdict

path = "monthwisePriceList.csv"
items = {}		#stores the mapping from id to item name
oldp = {} 		#stores the mapping from item id to the original price
newp = {}		#stores the mapping from item id to the new new price
cp = {}			#stores the mapping from item name to item id

#open the monthwiseprice list and populate the dicts
with open(path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		items[row[0]] = row[1]
		oldp[row[0]] = int(row[6])
		newp[row[0]] = int(row[6]) + min(0.1*oldp[row[0]],10)
		cp[row[1].strip()] = row[0]

data = defaultdict(list)	#dict to store the list of transactions for each segment
attr = [["Slot", "Item"],['d','d']]		#the presence of d tells Orange that the attribute is discrete for the application of A rules

#extracting transactions for each segment from August
csv_path = "augSales.csv"
with open(csv_path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		l = [0]*2; l1 = []	#l1 stores tuples of the form (Quantity,(Slot,ItenName))
		timestp = row[3].split(" ")[1]		#extracting the time of transaction
		slot = timestp[0:timestp.index(':')]
		l[0] = slot
		l[1] = items[row[1]]
		l1.append(int(row[2]))		
		l1.append(l)
		seg = row[5][0:2] if row[5][0:2] in ['F1','F2','F3','F4','F5','H1','H2'] else "oth"
		data[seg].append(l1)

#extracting transactions for each segment from September
csv_path = "sepSales.csv"
with open(csv_path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		l = [0]*2; l1 = []
		timestp = row[3].split(" ")[1]		
		slot = timestp[0:timestp.index(':')]
		l[0] = slot
		l[1] = items[row[1]]
		l1.append(int(row[2]))
		l1.append(l)
		seg = row[5][0:2] if row[5][0:2] in ['F1','F2','F3','F4','F5','H1','H2'] else "oth"
		data[seg].append(l1)

#extracting transactions for each segment from October
csv_path = "octSales.csv"
with open(csv_path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		l = [0]*2; l1 = []
		timestp = row[3].split(" ")[1]
		slot = timestp[0:timestp.index(':')]
		l[0] = slot
		l[1] = items[row[1]]
		l1.append(int(row[2]))
		l1.append(l)
		seg = row[5][0:2] if row[5][0:2] in ['F1','F2','F3','F4','F5','H1','H2'] else "oth"
		data[seg].append(l1)

#extracting transactions for each segment from November
csv_path = "novSales.csv"
with open(csv_path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		l = [0]*2; l1 = []
		timestp = row[3].split(" ")[1]
		slot = timestp[0:timestp.index(':')]
		l[0] = slot
		l[1] = items[row[1]]
		l1.append(int(row[2]))
		l1.append(l)
		seg = row[5][0:2] if row[5][0:2] in ['F1','F2','F3','F4','F5','H1','H2'] else "oth"
		data[seg].append(l1)

#write into F segment files
for i in range(1,6):
	path = "F"+str(i)+".csv"
	with open(path,"wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for at in attr:
			writer.writerow(at)
		for trans in data["F"+str(i)]:
			for qty in range(trans[0]):
				writer.writerow(trans[1])

#write into H segment files
for i in range(1,3):
	path = "H"+str(i)+".csv"
	with open(path,"wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for at in attr:
			writer.writerow(at)
		for trans in data["H"+str(i)]:
			for qty in range(trans[0]):
				writer.writerow(trans[1])

path = "OTHERS.csv"
with open(path,"wb") as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	for at in attr:
		writer.writerow(at)
	for trans in data["oth"]:
		for qty in range(trans[0]):
			writer.writerow(trans[1])

#make a read copy of newPrices.csv 
path = "newPrices.csv"
newPricesContent = []
with open(path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		newPricesContent.append(row)

path = "newPrices_read.csv"
with open(path, "wb") as csv_file:
	writer = csv.writer(csv_file, delimiter=',')
	writer.writerow(fields)
	for row in newPricesContent:
		writer.writerow(row)

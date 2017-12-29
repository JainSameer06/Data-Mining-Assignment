import csv
from rules import oldp, newp, items, cp, d
from collections import defaultdict

#comparator function for sorting each list of pairs (Slot,ItemId) stored in d
def cmpfn(x,y):
	return x[0]-y[0] if x[1]==y[1] else x[1]-y[1]

lt = ["F"+str(i) for i in range(1,6)] + ["H1","H2","OTHERS"]
#calculating the original revenue
old_rev = 0.0
csv_path = "decSales.csv"
with open(csv_path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		old_rev += (oldp[row[2]]*int(row[3]))

print "Old rev is ", old_rev

#calculating the new revenue after price modification
new_rev = 0.0
csv_path = "decSales.csv"
with open(csv_path, "rb") as fobj:
	reader = csv.reader(fobj)
	fields = reader.next()
	for row in reader:
		timestp = row[5].split(" ")[1]
		slot = int(timestp[0:timestp.index(':')])
		seg = row[4][0:2] if row[4][0:2] in ['F1','F2','F3','F4','F5','H1','H2'] else "OTHERS"
		if((slot,int(row[2])) in d[seg]): 
			new_rev += (newp[row[2]]*int(row[3]))
		else:
			new_rev += (oldp[row[2]]*int(row[3]))

print "New rev is ", new_rev
print "percent increase = ", (new_rev/old_rev-1)*100

#calculating the penalty
penalty = 0.0

for key,ls in d.iteritems():
	wt = {"F1":12,"F2":32,"F3":30,"F4":20,"F5":3,"H1":2,"H2":2,"OTHERS":1}[key]
	for i in range(len(ls)):
		ls[i] = (ls[i][0]+24,ls[i][1]) if ls[i][0] in [0,1,2] else ls[i]
	ls = sorted(ls, cmp=cmpfn)
	(a,b) = ls[0]; c = 1; iid = str(b)
	for i in range(1,len(ls)):
		if(b!=ls[i][1]):
			penalty += (c*c*(newp[iid]-oldp[iid])*wt)
			c = 1
		else:
			if(ls[i][0]-a==1):
				c += 1
			else:
				penalty += (c*c*(newp[iid]-oldp[iid])*wt)
				c = 1
		(a,b) = ls[i]
		iid = str(b)
	penalty += (c*c*(newp[iid]-oldp[iid])*wt)

print "Penalty = ", penalty

#Constructing newprice dictionary for convenient modification of newPrices.csv file
newprice = defaultdict(dict)	#key is the itemid and value is list of tuples of the form (slot, [seg list])
for iid in items.keys():
	newprice[int(iid)] = defaultdict(list)
for key,ls in d.iteritems():
	for i in range(len(ls)):
		ls[i] = (ls[i][0]+24,ls[i][1]) if ls[i][0] in [0,1,2] else ls[i]
	for a,b in ls:
		newprice[b][a].append(key)

#Modifying the newPrices.csv file 
csv_path = "newPrices.csv"
with open(csv_path, "wb") as fobj_w:
	with open("newPrices_read.csv", "rb") as fobj:
		reader = csv.reader(fobj)
		writer = csv.writer(fobj_w, delimiter=',')
		fields = reader.next()
		writer.writerow(fields)
		for row in reader:
			l = row[0:3]
			for sg in lt:
				if sg in newprice[int(row[0])][int(row[2])]:
					l.append(float(row[1]) + min(float(row[1])*0.1, 10))
				else:
					l.append(row[1])
			writer.writerow(l)

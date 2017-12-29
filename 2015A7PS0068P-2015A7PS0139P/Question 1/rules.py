from preprocess import oldp, newp, cp, items
import Orange
import operator
import csv

d = {}	#dictionary to store the best Association rules for each segment
lt = ["F"+str(i) for i in range(1,6)] + ["H1","H2","OTHERS"]

for segment in lt:
	data = Orange.data.Table(segment+".csv")	#loading data into Orange
	rules = Orange.associate.AssociationRulesInducer(data, support = 0.0001, confidence = 0.01, classificationRules = 1)
	l = []
	for r in rules:
		if(str(r.left[0])=='d'):
			continue
		iname = str(r.right[1]).strip(); iid = cp[iname]
		l.append((r.support, r.confidence, r, iid))

	l.sort(key=operator.itemgetter(0),reverse=True)			#sorting according to the support of the rule
	d[segment] = [(int(str(r[2].left[0])),int(r[3])) for r in l[0:48]] if segment in ['F2','F3','F4'] else [(int(str(r[2].left[0])),int(r[3])) for r in l[0:85]]

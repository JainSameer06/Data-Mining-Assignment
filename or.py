import Orange
from dmcode3 import r
data = Orange.data.Table("augToNovTrans.basket")
rules = Orange.associate.AssociationRulesSparseInducer(data, support = 0.0005)

#rules = Orange.associate.AssociationRulesSparseInducer(data, support = 0.00008)
i = 0
j = 0

lowRated = []
lowRatedNames = []

lowFreqNames = []

for item, freq in r.itemFrequency.iteritems():
	if freq < 1000:
		#print r.itemNumberToName[item], freq
		lowFreqNames.append(r.itemNumberToName[item])


for item in r.itemNumberToName:
	if item in r.ratingDict:
		#print r.itemNumberToName[item], item, r.ratingDict[item]
		if r.ratingDict[item] < 3:
			lowRated.append(item)
for item in lowRated:
	lowRatedNames.append(r.itemNumberToName[item])

#print lowRatedNames


def intersect (a, b):
	return list(set(a) & set(b))


for rule in rules:
	if(len(rule.left.get_metas(str)) + len(rule.right.get_metas(str))) > 2 and (len(rule.left.get_metas(str))==2):
		if len(intersect(rule.right.get_metas(str), lowRatedNames))> 0:
		#if len(intersect(rule.right.get_metas(str), lowFreqNames))> 0:
			print rule, rule.confidence, rule.support
			j+=1
	i+=1
print i, j


comboList = [["CHILLI PANEER", "Butter Naan", "Ice Cream Shake"], ["CHILLI PANEER", "Butter Naan", "PEPSI 600ML"], ["Chese Toast", "Plain Maggi", "Ice Cream Shake"], ["KADHAI PANEER", "Plain Maggi", "Butter Naan"], ["KADHAI PANEER", "Butter Naan", "Veg Rice"], ["KADHAI PANEER", "Butter Naan", "Ice Cream Shake"], ["KADHAI PANEER", "Butter Naan", "PULPY ORANGE"], ["KADHAI PANEER", "Butter Naan", "PEPSI 600ML"], ["Butter Chicken", "Butter Naan", "PULPY ORANGE"], ["Butter Chicken", "Butter Naan", "PEPSI 600ML"]]

print comboList

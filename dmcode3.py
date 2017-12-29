import csv
import copy

class Transaction:
	def __init__(self):
		self.itemList = []
		self.originalPrice = 0
		#self.appendItem(firstItem)

	def appendItem(self, item, price):
		self.itemList.append(item)
		self.originalPrice += price

	def getAllCombos(self, combols):
		l = []
		for combo in combols:
			lt = []
			mn = 1000
			for item in combo:
				lt.append(self.getcount(item))
				mn = min(mn, lt[-1])
			for num in range(mn):
				l.append(combo)
				for item in combo:
					self.itemList.remove(item)
		return l

	def getcount(self, comboItem):
		s = 0
		for item in self.itemList:
			if(item==comboItem):
				s += 1
		return s



class Reader:
	def __init__(self, salesFile, ratingFile, priceFile):
		self.salesFile = salesFile
		self.ratingFile = ratingFile
		self.priceFile = priceFile
		self.transactionList = []
		self.ratingDict = {}
		self.itemNumberToName = {}
		self.itemNameToNumber = {}
		self.itemFrequency = {}
		self.itemToPrice = {}
		self.comboList = [["CHILLI PANEER", "Butter Naan", "Ice Cream Shake"], ["CHILLI PANEER", "Butter Naan", "PEPSI 600ML"], ["Chese Toast", "Plain Maggi", "Ice Cream Shake"], ["KADHAI PANEER", "Plain Maggi", "Butter Naan"], ["KADHAI PANEER", "Butter Naan", "Veg Rice"], ["KADHAI PANEER", "Butter Naan", "Ice Cream Shake"], ["KADHAI PANEER", "Butter Naan", "PULPY ORANGE"], ["KADHAI PANEER", "Butter Naan", "PEPSI 600ML"], ["Butter Chicken", "Butter Naan", "PULPY ORANGE"], ["Butter Chicken", "Butter Naan", "PEPSI 600ML"]]


	def getComboDeduction(self, combo):
		original = 0
		for item in combo:
			original += float(self.itemToPrice[self.itemNameToNumber[item]])
		discount = ((20.0/len(combo))/100) * original
		return round((original - discount), 2)

	def getComboPrice(self, combo):
		price = 0.0
		for item in combo:
			price += float(self.itemToPrice[self.itemNameToNumber[item]])
		return price

	def getTotalDeduction(self):
		netDeduction = 0
		transactionListCopy = copy.deepcopy(self.transactionList)

		for transaction in transactionListCopy:
			billDiscount = 0
			combos = transaction.getAllCombos(self.comboList)
			for combo in combos:
				billDiscount += self.getComboDeduction(combo)
			netDeduction += billDiscount
		return netDeduction



	def getFrequencies(self):
		for item in self.ratingDict:
			self.itemFrequency[item] = 0
			for transaction in self.transactionList:
				if self.itemNumberToName[item] in transaction.itemList:
					self.itemFrequency[item] += 1



	def readPriceFile(self):
		with open(self.priceFile) as f:
			fileReader = csv.reader(f, delimiter = ",")
			for item in fileReader:
				self.itemNumberToName[item[0]] = item[1]
				self.itemNameToNumber[item[1]] = item[0]
				self.itemToPrice[item[0]] = item[6]


		#print self.itemNumberToName

	def readSalesFile(self):
		with open(self.salesFile) as f:
			fileReader = csv.reader(f, delimiter = ",")
			for itemSold in fileReader:
				#print itemSold
				if itemSold[0] == "BillNo":
					pass
				else:
					if itemSold[5] == "1":		#TransactionID == 1 means a new bill
						t = Transaction()
						for i in range(int(itemSold[2])):
							t.appendItem(self.itemNumberToName[itemSold[1]], int(self.itemToPrice[itemSold[1]]))
						self.transactionList.append(t)
						#self.transactionList.append(t)
						#print "If condition", len(self.transactionList)
					else:
						#print "Else condition", len(self.transactionList)
						for i in range(int(itemSold[2])):
							self.transactionList[len(self.transactionList) - 1].appendItem(self.itemNumberToName[itemSold[1]], int(self.itemToPrice[itemSold[1]]))
					


	def readRatingsFile(self):
		with open(self.ratingFile) as f:
			fileReader = csv.reader(f, delimiter = ",")

			firstRowFlag = 1
			currentItem = 0

			ratingSum = 0.0
			count = 0

			for itemSold in fileReader:
				if itemSold[0] == "BillNo":
					pass
				else:
					if firstRowFlag == 1:
						firstRowFlag = 0
						currentItem = itemSold[1]
						ratingSum = ratingSum + float(itemSold[7])
						count += 1
						#print "Inside condition 1"

					elif currentItem != itemSold[1]:
						self.ratingDict[currentItem] = round(ratingSum/count, 2)
						ratingSum = float(itemSold[7])
						count = 1
						currentItem = itemSold[1]

						#print "Inside condition 2", itemSold[0]

					else:
						ratingSum = ratingSum + float(itemSold[7])
						count += 1
						#print "Inside condition 3"

			self.ratingDict[currentItem] = round(ratingSum/count, 2)

	def printRatings(self):
		for item in self.ratingDict:
			print self.itemNumberToName[item], self.ratingDict[item]
			
			
					








class Writer:
	def __init__(self, r):
		with open("augToNovTrans.csv", "wb") as f:
			fileWriter = csv.writer(f, delimiter = ",")
			for transaction in r.transactionList:
				fileWriter.writerow(transaction.itemList)
		with open("q2Sol.csv", "wb") as g:
			fileWriter = csv.writer(g, delimiter = ",")
			#comboIdList = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
			i = 0
			for combo in r.comboList:
				if i == 0:
					fileWriter.writerow(["ComboId", "Old Price", "New Combo Price", "Item 1", "Item 2", "Item 3"])
					i += 1
					fileWriter.writerow([i] + [r.getComboPrice(combo)] + [r.getComboDeduction(combo)] + combo)

				else:
					i += 1
					fileWriter.writerow([i] + [r.getComboPrice(combo)] + [r.getComboDeduction(combo)] + combo)

			




#ratings = {}
def transactionSplitTester():
	#global ratings
	global r 
	r = Reader("augToNovSales.csv", "augToNovForRating.csv", "monthwisePriceList.csv")
	r.readPriceFile()
	r.readSalesFile()
	r.readRatingsFile()
	print r.ratingDict
	r.printRatings()
	r.getFrequencies()
	sum = 0.0
	for transaction in r.transactionList:
		sum += transaction.originalPrice
		#print transaction.originalPrice

	deduction = r.getTotalDeduction()
	print sum, deduction
	print deduction/sum * 100
	w = Writer(r)	
	#ratings = r.ratingDict
	print "Done"

	global dec
	dec = Reader("decSales.csv", "augToNovForRating.csv", "monthwisePriceList.csv")
	dec.readPriceFile()
	dec.readSalesFile()
	decSum = 0

	for transaction in dec.transactionList:
		decSum += transaction.originalPrice

	dec.ratingDict = r.ratingDict
	dec.itemNumberToName = r.itemNumberToName
	dec.itemNameToNumber = r.itemNameToNumber
	decDiscount = dec.getTotalDeduction()

	print decSum, decDiscount
	print decDiscount/decSum * 100

transactionSplitTester()

			


		

			

"""
	def getTotalDeduction(transactionList):
		netDeduction = 0
		transactionListCopy = copy.deepcopy(transactionList)

		for transaction in transactionListCopy:
			billDiscount = 0
			combos = transaction.getAllCombos(self.comboList)
			for combo in combos:
				billDiscount += self.getComboDeduction(combo)
			netDeduction += billDiscount
		return netDeduction

	decDiscount = getTotalDeduction(dec.transactionList)"""
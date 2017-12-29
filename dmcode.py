import csv


class Transaction:
	def __init__(self):
		self.itemList = []
		#self.appendItem(firstItem)

	def appendItem(self, item):
		self.itemList.append(item)


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
							t.appendItem(self.itemNumberToName[itemSold[1]])
						self.transactionList.append(t)
						#self.transactionList.append(t)
						#print "If condition", len(self.transactionList)
					else:
						#print "Else condition", len(self.transactionList)
						for i in range(int(itemSold[2])):
							self.transactionList[len(self.transactionList) - 1].appendItem(self.itemNumberToName[itemSold[1]])
					


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
	def __init__(self, transactionList):
		with open("augToNovTrans.csv", "wb") as f:
			fileWriter = csv.writer(f, delimiter = ",")
			for transaction in transactionList:
				fileWriter.writerow(transaction.itemList)



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
	print r.itemNameToNumber
	w = Writer(r.transactionList)	
	#ratings = r.ratingDict
	print "Done"

transactionSplitTester()

			


		

			

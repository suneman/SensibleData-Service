import json
import pymongo
from utils.log_database import LogDatabase
from utils import log_config as CONFIG

class LoggerInterface(object):

	logDatabase = None

	def __init__(self):
		self.logDatabase = LogDatabase()
#		configObj = open(self.configFile)
#		self.configs = json.load(configObj)	
#		self.logDatabase.collection = pymongo.Connection()[self.configs['PDS']][self.configs['PDSCollection']]
		

	def writeEntry(self, flowID, D, C, Y):
		self.logDatabase.collection.insert({"flowID" : flowID, "D": D, "C" : C , "Y" : Y})

	def writeEntryWithMAC(self, flowID, D, C, Y, Z, A):
		self.logDatabase.collection.insert({"flowID" : flowID, "D": D, "C" : C , "Y" : Y, "Z" : Z, "A" : A})


	def getMaxFlowID(self):
		if (self.logDatabase.collection.count() < 1):
			return 1
		else:
			resultEntry = self.logDatabase.collection.find_one(sort=[("flowID", -1)])
			return resultEntry['flowID']


# TODO:
	def getMaxUserAppFlow(self, userID, appID):
		return self.logDatabase.collection.find().sort("userAppFlow", pymongo.DESCENDING).count()

	
	def getPrevious(self, flowID):
		previous = flowID - 1
		result = self.logDatabase.collection.find_one({"flowID" : previous})
		return result

	def getEntry(self, flowID):
		result = self.logDatabase.collection.find_one({"flowID" : flowID})
		return result

	def getAuthenticationKey(self, flowID):
		result = self.logDatabase.collection.find({"flowID" : flowID})
		# Some sanity checks and early returns
		if (result is None or result.count() == 0):
			print "flowID = " + str(flowID) + " not found"
			return -1
		elif (result.count() > 1):
			print "More than ONE authentication key A for flowID = " + str(flowID)
			return -2
		elif (result.count() == 1):
			return self.logDatabase.collection.find_one({"flowID" : flowID}).get("A") # Retrieve the Authentication key used for that event


	def getLastEntry(self, userID):
#		return self.logDatabase.collection.find({"D.userID" : userID}, sort=[("D.userAppFlow", pymongo.DESCENDING)]).limit(1)
		return self.logDatabase.collection.find_one({"D.userID" : userID}, sort=[("D.userAppFlow", pymongo.DESCENDING)])

	def count(self, userID):
		return self.logDatabase.collection.find({"D.userID" : userID}).count()

	def getAllFlowIDs(self, userID):
		return self.logDatabase.collection.find({"D.userID" : userID}, {"flowID" : 1, "_id" : 0}, sort=[("flowID", pymongo.DESCENDING)])

	def getDataForCheck(self, flowID):
		if (flowID < 1):
			print "flowID = " + str(flowID) + " can not be checked"
			exit(-1)
		current = self.logDatabase.collection.find({"flowID" : flowID}).limit(1) #refactor
		current_D = None
		current_C = None
		current_Y = None
		for item in current: #refatcor
			current_D = item["D"]
			current_C = item["C"]
			current_Y = item["Y"]
		return {"current_D" : current_D, "current_C" : current_C,  "current_Y": current_Y}

	def getPublicSeed(self):
		return CONFIG.SEED

	def getLastY(self):
		maxFlowID = self.getMaxFlowID()
		lastEntry = self.getEntry(maxFlowID)
		toReturn = lastEntry.get("Y")
		print toReturn

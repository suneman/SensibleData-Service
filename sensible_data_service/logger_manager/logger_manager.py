import pymongo
#import service_config
#import SECURE_service_config
from utils.log_database import LogDatabase
import json
from utils import log_config as CONFIG
from Crypto.Hash import HMAC
from Crypto.Hash import SHA512
import Helper

class Logger(object):

	logDatabase = None

	A0 = None
	D0 = None
	Dj = None
	Yj = None
	Yj_1 = None
	Zj = None
	Zj_1 = None

# For test:
	userID = "riccardo"
	initialUserAppflowID = 0


	def __init__(self):
		self.logDatabase = LogDatabase()
		self.A0 = CONFIG.A0
#		self.A0 = str(configs['A0']).encode("utf-8") # encoding in utf-8 format

		self.SEED = CONFIG.SEED
#		self.SEED = str(configs['SEED']).encode("utf-8")
#		self.D0 = configs['D0']
		self.D0 = CONFIG.D0
#		self.logDatabase = pymongo.Connection()[self.configs['PDS']][self.configs['PDSCollection']]
		self.cryptoSetup()		



# In this case, Y is NOT the hash of the current D0 with the previous link, but a random seed.
# D0 is useless, added to make a consistent entry in the log, not used for authentication.
# Z0 is the HashMAC of SEED. This is the farest link that chan be checked in the chain. If HMAC_A0(SEED) == myValue, ok.
	def cryptoSetup(self): # make an overloaded method used also by the normal creation, for the "D payload"
		h = HMAC.new(key=self.A0, msg=self.SEED,digestmod=SHA512) # Load the HMAC with the secret key A0, want to hash SEED, hash algo = SHA512
		self.Z0 = h.hexdigest().encode("utf-8") # The result is stored in Z = HMAC of SEED with the key A0 ==> Z=HMAC_A0_(SEED)
		C = Helper.computeChecksum([self.D0])
		D = {"payload" : self.D0['payload'], "userID" : self.userID, "userAppFlow" : str(self.initialUserAppflowID), "appID" : self.D0['appID']} # Creates D for the first dummy entry
		self.writeEntry(0, D, C, self.SEED) # Write the first [dummy] entry in the log + the authentication key [before being overridden]


# data = <userID,appID,payload>
# Make the fileds dynamically read from the config file instead of hardcoded.
	def createDforlog(self, data):
		userID = data['userID']
		appID = data['appID']
		payload = data['payload']
		userAppFlow = self.getMaxUserAppFlow(userID, appID)
		return {"userID" : userID, "userAppFlow" : userAppFlow, "appID" : appID, "payload" : payload}




# Entry = <flowID, D, current_C, current_Y>
#	def createLogEntry(self, data):
	def append(self, data):
		flowID = self.getMaxFlowID() + 1		
		D = self.createDforlog(data)
		current_C = Helper.createC(D)
		previous_Y = self.getEntry(flowID - 1).get("Y")
		current_Y = Helper.computeY(previous_Y, current_C)
		self.writeEntry(flowID, D, current_C, current_Y)	# Finally, writes the log entry

	def writeEntry(self, flowID, D, C, Y):
		jsonObj = {"flowID" : flowID, "D": D, "C" : C , "Y" : Y}
		returned_id = self.logDatabase.insert( jsonObj )
		print returned_id

	def writeEntryWithMAC(self, flowID, D, C, Y, Z, A):
		self.logDatabase.insert({"flowID" : flowID, "D": D, "C" : C , "Y" : Y, "Z" : Z, "A" : A})


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
		result = self.logDatabase.find_one({"flowID" : previous})
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
#		return self.logDatabase.find({"D.userID" : userID}, sort=[("D.userAppFlow", pymongo.DESCENDING)]).limit(1)
		return self.logDatabase.collection.find_one({"D.userID" : userID}, sort=[("D.userAppFlow", pymongo.DESCENDING)])


	def count(self, userID):
		return self.logDatabase.find({"D.userID" : userID}).count()


	def getAllFlowIDs(self, userID):
		return self.logDatabase.find({"D.userID" : userID}, {"flowID" : 1, "_id" : 0}, sort=[("flowID", pymongo.DESCENDING)])


	def getDataForCheck(self, flowID):
		if (flowID < 1):
			print "flowID = " + str(flowID) + " can not be checked"
			exit(-1)
		current = self.logDatabase.find({"flowID" : flowID}).limit(1) #refactor
		current_D = None
		current_C = None
		current_Y = None
		for item in current: #refatcor
			current_D = item["D"]
			current_C = item["C"]
			current_Y = item["Y"]
		return {"current_D" : current_D, "current_C" : current_C,  "current_Y": current_Y}


	def getPublicSeed(self):
		return self.configs['SEED']


	def getLastY(self):
		maxFlowID = self.getMaxFlowID()
		lastEntry = self.getEntry(maxFlowID)
		toReturn = lastEntry.get("Y")
		print toReturn


# TODO:
#	def getLast
#	def getFirst

#	def publishLastY(self):
#		return self.getLastY()
























import pymongo
import service_config
import EXAMPLE_SECURE_service_config as SECURE_service_config
import log_config
from utils import log_config as CONFIG


class LogDatabase(object):

	client = None
	db = None
	collection = None

        def __init__(self):
                self.client = pymongo.MongoClient(log_config.LOGGER_DATABASE['params']['url']%(log_config.LOGGER_DATABASE['params']['username'],log_config.LOGGER_DATABASE['params']['password']))
		self.db = self.client[log_config.LOGGER_DATABASE['params']['database']]
		self.collection = self.db[log_config.LOGGER_DATABASE['params']['collection']]



	def insert(self, document):
		doc_id = self.collection.insert(document)
		return doc_id

	def getDocuments(self, query, collection):
		coll = self.db[collection]
		return coll.find(query)

        def writeEntry(self, flowID, D, C, Y):
                returned = self.collection.insert({"flowID" : flowID, "D": D, "C" : C , "Y" : Y})
		print "returned = " + str(returned)

        def writeEntryWithMAC(self, flowID, D, C, Y, Z, A):
                self.collection.insert({"flowID" : flowID, "D": D, "C" : C , "Y" : Y, "Z" : Z, "A" : A})


        def getMaxFlowID(self):
		maxFlowID = 0
		resultEntry = self.collection.find_one(sort=[("flowID", -1)])
		if (resultEntry is not None):
			maxFlowID = resultEntry['flowID']
		print "maxFLowID = " + str(maxFlowID)
		return maxFlowID


# TODO:
        def getMaxUserAppFlow(self, userID, appID):
                return self.collection.find().sort("userAppFlow", pymongo.DESCENDING).count()

        
        def getPrevious(self, flowID):
                previous = flowID - 1
                result = self.collection.find_one({"flowID" : previous})
                return result

        def getEntry(self, flowID):
		print "flowID = " + str(flowID)
                result = self.collection.find_one({"flowID" : flowID})
                return result

        def getAuthenticationKey(self, flowID):
                result = self.collection.find({"flowID" : flowID})
                # Some sanity checks and early returns
                if (result is None or result.count() == 0):
                        print "flowID = " + str(flowID) + " not found"
                        return -1
                elif (result.count() > 1):
                        print "More than ONE authentication key A for flowID = " + str(flowID)
                        return -2
                elif (result.count() == 1):
                        return self.collection.find_one({"flowID" : flowID}).get("A") # Retrieve the Authentication key used for that event

        def getLastEntry(self, userID):
#               return self.collection.find({"D.userID" : userID}, sort=[("D.userAppFlow", pymongo.DESCENDING)]).limit(1)
                return self.collection.find_one({"D.userID" : userID}, sort=[("D.userAppFlow", pymongo.DESCENDING)])

        def count(self, userID):
                return self.collection.find({"D.userID" : userID}).count()

        def getAllFlowIDs(self, userID):
                return self.collection.find({"D.userID" : userID}, {"flowID" : 1, "_id" : 0}, sort=[("flowID", pymongo.DESCENDING)])

        def getDataForCheck(self, flowID):
                if (flowID < 1):
                        print "flowID = " + str(flowID) + " can not be checked"
                        exit(-1)
                current = self.collection.find({"flowID" : flowID}).limit(1) #refactor
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

# TODO: if there are NO entries, it crashes.
        def getLastY(self):
		maxFlowID = self.getMaxFlowID()
                lastEntry = self.getEntry(maxFlowID)
                toReturn = lastEntry.get("Y")
		return toReturn

	

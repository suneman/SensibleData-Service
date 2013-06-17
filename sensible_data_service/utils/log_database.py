import pymongo
import service_config
import log_config
from utils import log_config as CONFIG
from loggerApp import helperModule


# SQL <==> NoSQL
# Table <==> Collection
# Column <==> Field
# Entry <==> Document


# Log entry = <flowID, D, V, Z> TODO: use the models as proxies!

class LogDatabase(object):

	client = None
	db = None
        collectionList = None

        def __init__(self):
            self.client = pymongo.MongoClient(log_config.LOGGER_DATABASE['params']['url']%(log_config.LOGGER_DATABASE['params']['username'],log_config.LOGGER_DATABASE['params']['password']))
            self.db = self.client[log_config.LOGGER_DATABASE['params']['database']]


        def createCollection(self, _username):
            collectionName = _username
            self.writeEntry(collectionName, CONFIG.FIRST_ENTRY, CONFIG.D0, CONFIG.V0, CONFIG.Z0) # Seed entry for a given user
            return None


        def writeEntry(self, _collectionName, flowID, D, V, Z):
            returned = self.db[_collectionName].insert({"flowID" : flowID, "D" : D, "V" : V, "Z" : Z})
            return str(returned)


        def getMaxFlowID(self, _collectionName):
            maxFlowID = 0
            resultEntry = self.db[_collectionName].find_one(sort=[("flowID", -1)])
            if (resultEntry is not None):
                maxFlowID = resultEntry['flowID']
            return maxFlowID


        def getPrevious(self, _collectionName, flowID):
            previous = flowID - 1
            return self.db[_collectionName].find_one({"flowID" : previous})


        def getLast_Z(self, _collectionName):
            maxFlowID = self.getMaxFlowID(_collectionName)
            return self.getEntry(_collectionName, maxFlowID).get("Z")


        def getEntry(self, _collectionName, flowID):
            return self.db[_collectionName].find_one({"flowID" : flowID})


# TODO: create Z0 at createCollection moment, not static
        def getZ0(self):
            return CONFIG.Z0



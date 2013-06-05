from pymongo import MongoClient
import service_config
import EXAMPLE_SECURE_service_config as SECURE_service_config

class LogDatabase(object):

	client = None
	db = None


        def __init__(self):
                self.client = MongoClient(service_config.LOGGER_DATABASE['params']['url']%(SECURE_service_config.LOGGER_DATABASE['username'],SECURE_service_config.LOGGER_DATABASE['password']))
                self.db = self.client[service_config.LOGGER_DATABASE['params']['database']]

	def insert(self, document, collection):
		coll = self.db[collection]
		doc_id = coll.insert(document)
		return doc_id

	def getDocuments(self, query, collection):
		coll = self.db[collection]
		return coll.find(query)
		

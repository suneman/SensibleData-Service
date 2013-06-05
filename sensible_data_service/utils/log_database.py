from pymongo import MongoClient
import service_config
import EXAMPLE_SECURE_service_config as SECURE_service_config
import log_config

class LogDatabase(object):

	client = None
	db = None
	collection = None

        def __init__(self):
                self.client = MongoClient(log_config.LOGGER_DATABASE['params']['url']%(log_config.LOGGER_DATABASE['params']['username'],log_config.LOGGER_DATABASE['params']['password']))
		self.db = self.client[log_config.LOGGER_DATABASE['params']['database']]
		self.collection = self.db[log_config.LOGGER_DATABASE['params']['collection']]



	def insert(self, document):
		doc_id = self.collection.insert(document)
		return doc_id

	def getDocuments(self, query, collection):
		coll = self.db[collection]
		return coll.find(query)
		

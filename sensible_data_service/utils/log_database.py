from pymongo import MongoClient
import service_config
#import SECURE_service_config

class LogDatabase(object):

	client = None
	db = None


        def __init__(self):
                self.client = MongoClient(service_config.LOGGER_DATABASE['params']['url']%(SECURE_service_config.LOGGER_DATABASE['username'],SECURE_service_config.LOGGER_DATABASE['password']))
                self.db = self.client[service_config.LOGGER_DATABASE['params']['database']]

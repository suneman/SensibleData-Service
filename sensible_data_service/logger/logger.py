from pymongo import MongoClient
import service_config
import SECURE_service_config
from utils.log_database import LogDatabase

class Logger(object):

	logDatabase = None

	def __init__(self):
			self.logDatabase = LogDatabase()

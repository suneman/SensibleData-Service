import pymongo
import service_config
import log_config
from utils import log_config as CONFIG
from loggerApp import helperModule

class Keystore(object):

    keytable = None

    def __init__(self):
        self.client = pymongo.MongoClient(log_config.LOGGER_DATABASE['params']['url']%(log_config.LOGGER_DATABASE['params']['username'],log_config.LOGGER_DATABASE['params']['password']))
        self.db = self.client[log_config.LOGGER_DATABASE['params']['database']]
        self.keytable = self.db[log_config.LOGGER_KEYS['params']['collection']]

    def addUserKey(self, _username, _key):
        return self.keytable.insert({"username": _username, "key" : _key})

    def getUserKey(self, _username):
        return self.keytable.find_one({"username" : _username}).get("key")

    def reset(self):
        return self.keytable.remove()

    def update_A(self, _username):
        A = self.getUserKey(_username)
        A = helperModule.calculateHash_A(1,A)
        self.keytable.update({ "username": _username }, { "$set": { "key": A } } )
        return True # TODO change with more useful

# TODO: check if "count" has good performance
    def existsUser(self, _username):
        exists = False
        if (self.keytable.find({ "username": _username}).count() != 0):
            exists = True
        return exists

# TODO: add a check to see if has been deleted or not.
    def deleteUser(self, _username):
        return self.keytable.remove({"username" : _username})

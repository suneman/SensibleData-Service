import pymongo
from utils.log_database import LogDatabase
import json
from utils import log_config as CONFIG
from Crypto.Hash import SHA512
import helperModule
import PERMISSIONS
import time
import datetime
from utils.keystore import Keystore

class Logger(object):

    logDatabase = None
    keystore = None

    def __init__(self):
        self.logDatabase = LogDatabase()
        self.keystore = Keystore()

    def cryptoSetup(self):
        self.logDatabase.writeEntryWith_Z(CONFIG.FIRST_ENTRY, CONFIG.D0, CONFIG.V0, CONFIG.Z0)

    def addUserKey(self, _username, _key):
        mid = self.keystore.addUserKey(_username, _key)        
        return (mid, " ", _key)

# log_entry = <flowID, D, V, Z>
# D = <userID,appID,payload>
    def append_dataflow(self, _username, _data):
        current_flowID = self.logDatabase.getMaxFlowID() + 1		
        current_D = helperModule.create_D(_data)
        current_V = helperModule.create_V(current_D)
        
        previous_A = self.keystore.getUserKey(_username)
        previous_Z = self.logDatabase.getPrevious(current_flowID).get("Z")
        current_Z = helperModule.create_Z(current_V, previous_Z, str(previous_A))
        
        self.keystore.update_A(_username)

        mongo_id_string = self.logDatabase.writeEntryWith_Z(current_flowID, current_D, current_V, current_Z) # Finally, writes the log entry
        return (current_flowID, mongo_id_string)


    def dispatching(self,role,method):
        granted = False
        for case in self.switch(role):
            if case(PERMISSIONS.USER_ID):
                granted = self.checkPermissions(method,PERMISSIONS.USER["methods"])
                return granted
            if case(PERMISSIONS.ADMIN_ID):
                granted = sel.fcheckPermissions(method,PERMISSIONS.ADMIN["methods"])
                return granted
            if case():
                granted = False
                print "Oh no, the case = <" + role + "," + method + "> is not possible!"


    def checkPermissions(self, method, methodList):
        granted = False
        if method in methodList:
            granted = True
        else:
            granted = False
        return granted
                        

    class switch(object):
        def __init__(self, value):
            self.value = value
            self.fall = False
        def __iter__(self): 
            yield self.match
            raise StopIteration
        def match(self, *args):
            if self.fall or not args:
                return True
            elif self.value in args:
                self.fall = True
                return True
            else:
                return False


    def append(self, role, _username, method, _data):
            returned = None
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') # Format : "2013-06-08 12:01:15"
            if (self.dispatching(role, method)): # If the check went fine
                returned = getattr(self, method)(_username, _data) # the corresponding method gets called with data as input
                if not method:
                    raise Exception("Method %s not implemented" % method_name)
            else:
                print st + " ==> role = <" + role + "> has NO permission for method = <" + method + ">" 
            return returned


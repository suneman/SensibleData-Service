import pymongo
from utils.log_database import LogDatabase
import json
from utils import log_config as CONFIG
from Crypto.Hash import SHA512
import helperModule
from utils.keystore import Keystore
from django.contrib.auth.decorators import user_passes_test
import bson.json_util as json
from django.http import HttpResponse

class Logger(object):

    logDatabase = None
    keystore = None
    flowID_to_end = 1

    def __init__(self):
        self.logDatabase = LogDatabase()
        self.keystore = Keystore()


# Get request, check permissions, create pair in keystore, start the log
    def createNewUser(self, _request, newUser, newBaseKey):
        if not helperModule.isSuperUser(_request):
            return False
        if self.keystore.existsUser(newUser): # Only if the user is not already in the db
            print "User already present in th DB"
            return False
        self.keystore.addUserKey(newUser, newBaseKey) # Add new pair <user, key>
        self.logDatabase.createCollection(newUser) # Start the log
        return "Created"


# TODO: ask for the direction. Look at the model of entry to see the required fields.
    def append(self, _request, _data): # who is requesting to append, the data to append, who are we talking about
        if not helperModule.permissionCheck(_request, "loggerApp.auditEntry_append"):
            return False
        _username = str(_request.user)
        if not self.keystore.existsUser(_username): # Integrate this check in the previous one
            return False
        st = helperModule.getTimestamp() # add this in the log entry
        current_flowID = self.logDatabase.getMaxFlowID(_username) + 1		
        current_D = helperModule.create_D(_username, _data)
        current_V = helperModule.create_V(current_D)
        previous_A = self.keystore.getUserKey(_username)
        previous_Z = self.logDatabase.getPrevious(_username, current_flowID).get("Z")
        current_Z = helperModule.create_Z(current_V, previous_Z, str(previous_A))
        self.keystore.update_A(_username) # evolve the key
        mongo_id_string = self.logDatabase.writeEntry(_username, current_flowID, current_D, current_V, current_Z)
        return (current_flowID, " ", mongo_id_string)


    def userRegistration(self, _registered, _secretKey): # _registered = True/False
        pass

    def appAuthorized(self, _authorized, _appName, _request):
        pass


    def deleteUser(self, _request):
        if not helperModule.isSuperUser(_request):
            return False
        username = _request.GET.get("username")
        return self.keystore.deleteUser(username)
        

    def updateUserKey(self, _request): # In case get lost
        pass

       
    def check(self, _request, _key):
        if not helperModule.permissionCheck(_request, "loggerApp.auditTrail_verify"):
            return False
        username = str(_request.user)
        if not self.keystore.existsUser(username): # Integrate this check in the previous one
            return False
        return self.startCheck_Z(username, self.logDatabase.getZ0(), self.logDatabase.getLast_Z(username), self.flowID_to_end, _key)


    def checkGroup(self, _request, _group_name):
        groups_ValuesListQuerySet = _request.user.groups.values_list('name',flat=True)
        groups_list = list(groups_ValuesListQuerySet)
        in_group = False
        if _group_name in groups_list:
            in_group = True
        return in_group


    def dataIntegrityCheck(self,current_D, current_V):
        status = False # false=KO, True=OK
        temp_V = helperModule.create_V(current_D)
        if (temp_V == current_V):
                status = True
        return {"status" : status, "temp_V" : temp_V}


    def chainIntegrityCheck_Z(self, previous_Z, current_V, current_Z, A, flowID):
        status = False # false=KO, True=OK
        previous_A = helperModule.calculateHash_A(flowID-1, A)
        temp_Z = helperModule.create_Z(current_V, previous_Z, previous_A)
        if ( temp_Z == current_Z):
                status = True
        return {"status" : status, "temp_Z" : temp_Z}


    def startCheck_Z(self, username, previous_Z, Z_last, flowID, A):
        keepLooking = True
        audit = {}
        while ( (flowID <= self.logDatabase.getMaxFlowID(username)) and (keepLooking==True) ):
            dataForCheck = self.getDataForCheck(username, flowID)
            integrityDict = self.dataIntegrityCheck(dataForCheck["current_D"], dataForCheck["current_V"])
            if ( not integrityDict["status"] ):
                keepLooking = False
            chainDict = self.chainIntegrityCheck_Z(previous_Z, dataForCheck["current_V"], dataForCheck["current_Z"], A, flowID)
            if ( not chainDict["status"] ):
                keepLooking = False
            audit = {flowID : [integrityDict["status"], chainDict["status"]]}
            previous_Z = chainDict["temp_Z"]
            flowID = flowID + 1
        return audit


    def getDataForCheck(self, username, flowID):
        if (flowID < 1):
            print "flowID = " + str(flowID) + " can not be checked"
            exit(-1)
        current = self.logDatabase.getEntry(username, flowID)
        return {"current_D" : current.get("D"), "current_V" : current.get("V"),  "current_Z" : current.get("Z")}



####################################################
# Call examples:

def createNewUser(request):
    logger = Logger()
    user = request.GET.get("user")
    key = request.GET.get("key")
    returned = logger.createNewUser(request, user, key) # Call this
    return HttpResponse(returned)


def append(request):
    logger = Logger()
    fakeJson = {"appID": "FUNF", "payload": "FUNF_dummyPayload"} # get this from caller
    returned = logger.append(request, fakeJson)
    return HttpResponse(returned)


def check(request):
    key = request.GET.get("key") # Get from the caller 
    logger = Logger()
    returned = logger.check(request, key)
    return HttpResponse(returned)



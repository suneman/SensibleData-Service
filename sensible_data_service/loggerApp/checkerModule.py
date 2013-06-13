import helperModule
from utils import log_database
from utils import log_config as CONFIG

class Checker(object):

    log = None
    flowd_id_to_end = 1

    def __init__(self):
        self.log = log_database.LogDatabase()


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


    def startCheck_Z(self, previous_Z, Z_last, flowID, A):
        keepLooking = True
        audit = {}
        while ( (flowID <= self.log.getMaxFlowID()) and (keepLooking==True) ):
            dataForCheck = self.getDataForCheck(flowID)
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

    def check_Z(self):
        Z_seed = self.log.getZ0().encode("utf-8").strip(' \t\n\r') 
        Z_last = self.log.getLast_Z().encode("utf-8").strip(' \t\n\r') 
        A0 = CONFIG.A0.encode("utf-8").strip(' \t\n\r')  
        flowID = self.flowd_id_to_end
        return self.startCheck_Z(Z_seed, Z_last, flowID, A0)


    def getDataForCheck(self, flowID):
        if (flowID < 1):
            print "flowID = " + str(flowID) + " can not be checked"
            exit(-1)
        current = self.log.getEntry(flowID) #refactor
        return {"current_D" : current.get("D"), "current_V" : current.get("V"),  "current_Z" : current.get("Z")}

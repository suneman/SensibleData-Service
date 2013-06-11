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


#	def chainIntegrityCheck(self, previous_Y, current_V, current_Y):
#		status = False # false=KO, True=OK
#		temp_Y = helperModule.create_Y(previous_Y, current_V)
#		if ( temp_Y == current_Y):
#			status = True
#		return {"status" : status, "temp_Y" : temp_Y}

        def chainIntegrityCheck_Z(self, previous_Z, current_V, current_Z, previous_A):
		status = False # false=KO, True=OK
		temp_Z = helperModule.create_Z(current_V, previous_Z, previous_A)
                print "current_V = " + current_V
                print "previous_A = " + previous_A
                print "previous_Z = " + previous_Z
                print "current_Z = " + current_Z
                print "temp_Z = " + temp_Z
		if ( temp_Z == current_Z):
			status = True
		return {"status" : status, "temp_Z" : temp_Z}




	def startCheck_Z(self, previous_Z, Z_last, flowID, previous_A):
		keepLooking = True
		verifiedFlowID = 0
		audit = {}
		while ( (previous_Z != Z_last) and (keepLooking==True) ):
			dataForCheck = self.log.getDataForCheck(flowID)

			integrityDict = self.dataIntegrityCheck(dataForCheck["current_D"], dataForCheck["current_V"])
			if ( not integrityDict["status"] ):
				keepLooking = False

                        print
                        print "flowID = " + str(flowID)
			chainDict = self.chainIntegrityCheck_Z(previous_Z, dataForCheck["current_V"], dataForCheck["current_Z"], dataForCheck["previous_A"])
			if ( not chainDict["status"] ):
				keepLooking = False
			
			audit = {flowID : [integrityDict["status"], chainDict["status"]]}

			previous_Z = chainDict["temp_Z"]
			flowID = flowID + 1

		return audit

#        def startCheck(self, Y_1, Y_last, flowID):
#                        keepLooking = True
#                        verifiedFlowID = 0
#                        audit = {}
#                        while ( (Y_1 != Y_last) and (keepLooking==True) ):
#                                dataForCheck = self.log.getDataForCheck(flowID)
#                                integrityDict = self.dataIntegrityCheck(dataForCheck["current_D"], dataForCheck["current_V"])
#                                
#                                if ( not integrityDict["status"] ):
#                                        keepLooking = False
#                
#                                chainDict = self.chainIntegrityCheck(Y_1, integrityDict["temp_V"], dataForCheck["current_Y"])
#
#                                if ( not chainDict["status"] ):
#                                        keepLooking = False
#                                
#                                audit = {flowID : [integrityDict["status"], chainDict["status"]]}
#
#                                Y_1 = chainDict["temp_Y"]
#                                flowID = flowID + 1
#
#                        return audit
#
#
#        def check(self):
#                Y_seed = self.log.getPublicSeed()
#                Y_last = self.log.getLastY()
#                flowID = self.flowd_id_to_end
#                return self.startCheck(Y_seed, Y_last, flowID) #where I start, where I need to end up
            
        def check_Z(self):
            Z_seed = self.log.getZ0()
            Z_last = self.log.getLast_Z()
            A0 = self.log.getA0()
            flowID = self.flowd_id_to_end
            return self.startCheck_Z(Z_seed, Z_last, flowID, A0) #where I start, where I need to end up


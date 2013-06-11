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


        def chainIntegrityCheck_Z(self, previous_Z, current_V, current_Z):
		status = False # false=KO, True=OK

                previous_A = helperModule.read_A()


		temp_Z = helperModule.create_Z(current_V, previous_Z, previous_A)
                print "previous_A = " + previous_A
                print "previous_Z = " + previous_Z
                print "current_Z = " + current_Z
                print "temp_Z = " + temp_Z
		if ( temp_Z == current_Z):
			status = True
		return {"status" : status, "temp_Z" : temp_Z}


	def startCheck_Z(self, previous_Z, Z_last, flowID, A):
		keepLooking = True
		verifiedFlowID = 0
		audit = {}
		while ( (previous_Z != Z_last) and (keepLooking==True) ):
			dataForCheck = self.log.getDataForCheck(flowID)
                        print "dataForCheck = " 
                        print dataForCheck
			integrityDict = self.dataIntegrityCheck(dataForCheck["current_D"], dataForCheck["current_V"])
			if ( not integrityDict["status"] ):
				keepLooking = False
                        print
                        print "flowID = " + str(flowID)
			chainDict = self.chainIntegrityCheck_Z(previous_Z, dataForCheck["current_V"], dataForCheck["current_Z"])
			if ( not chainDict["status"] ):
				keepLooking = False
			
			audit = {flowID : [integrityDict["status"], chainDict["status"]]}

			previous_Z = chainDict["temp_Z"]
			flowID = flowID + 1

		return audit

        def check_Z(self):
            Z_seed = self.log.getZ0()
            Z_last = self.log.getLast_Z()
            flowID = self.flowd_id_to_end
            return self.startCheck_Z(Z_seed, Z_last, flowID, CONFIG.A0)


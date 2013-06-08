import helperModule
from utils import log_database

class Checker(object):

	log = None
	flowd_id_to_end = 1

	def __init__(self):
		self.log = log_database.LogDatabase()


	def dataIntegrityCheck(self,current_D, current_C):
		status = False # false=KO, True=OK
		temp_C = helperModule.create_C(current_D)
		if (temp_C == current_C):
			status = True
		return {"status" : status, "temp_C" : temp_C}


	def chainIntegrityCheck(self, previous_Y, current_C, current_Y):
		status = False # false=KO, True=OK
		temp_Y = helperModule.create_Y(previous_Y, current_C)
		if ( temp_Y == current_Y):
			status = True
		return {"status" : status, "temp_Y" : temp_Y}


	def startCheck(self, Y_1, Y_last, flowID):
		keepLooking = True
		verifiedFlowID = 0
		audit = {}
		while ( (Y_1 != Y_last) and (keepLooking==True) ):
			dataForCheck = self.log.getDataForCheck(flowID)
			integrityDict = self.dataIntegrityCheck(dataForCheck["current_D"], dataForCheck["current_C"])
			
			if ( not integrityDict["status"] ):
				keepLooking = False
	
			chainDict = self.chainIntegrityCheck(Y_1, integrityDict["temp_C"], dataForCheck["current_Y"])

			if ( not chainDict["status"] ):
				keepLooking = False
			
			audit = {flowID : [integrityDict["status"], chainDict["status"]]}

			Y_1 = chainDict["temp_Y"]
			flowID = flowID + 1

		return audit

	def check(self):
		Y_seed = self.log.getPublicSeed()
		Y_last = self.log.getLastY()
		flowID = self.flowd_id_to_end
		return self.startCheck(Y_seed, Y_last, flowID) #where I start, where I need to end up

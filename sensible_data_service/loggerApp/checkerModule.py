import helperModule
from utils import log_database

class Checker(object):

	log = None

	def __init__(self):
		self.log = log_database.LogDatabase()


	def dataIntegrityCheck(self,current_D, current_C):
		status = False # false=KO, True=OK
		temp_C = helperModule.createC(current_D)
		if (temp_C == current_C):
			status = True
		return {"status" : status, "temp_C" : temp_C}


	def chainIntegrityCheck(self, previous_Y, current_C, current_Y):
		status = False # false=KO, True=OK
		temp_Y = helperModule.computeY(previous_Y, current_C)
		if ( temp_Y == current_Y):
			status = True
		return {"status" : status, "temp_Y" : temp_Y}


	def startCheck(self, Y_1, Y_last, flowID):
		keepLooking = True
		verifiedFlowID = 0
		audit = {}
		while ( (Y_1 != Y_last) and (keepLooking==True) ):
#			print
			dataForCheck = self.log.getDataForCheck(flowID)
			integrityDict = self.dataIntegrityCheck(dataForCheck["current_D"], dataForCheck["current_C"])
			
#			print "flowID=" + str(flowID) + ", dataIntegrityCheckPassed? "+ str(integrityDict["status"])
			if ( not integrityDict["status"] ):
				keepLooking = False
	
			chainDict = self.chainIntegrityCheck(Y_1, integrityDict["temp_C"], dataForCheck["current_Y"])
#			print "flowID=" + str(flowID) + ", chainIntegrityCheck? "+ str(chainDict["status"])
			if ( not chainDict["status"] ):
				keepLooking = False
			
			audit = {flowID : [integrityDict["status"], chainDict["status"]]}

			Y_1 = chainDict["temp_Y"]
			flowID = flowID + 1

#		print "Max flowID verified = " + str(flowID - 1)
#		print audit
		return audit

# TODO: REFACTOR flowID = 1 to terminate
	def check(self):
		Y_seed = self.log.getPublicSeed()
		Y_last = self.log.getLastY()
		flowID = 1
		return self.startCheck(Y_seed, Y_last, flowID) #where I start, where I need to end up

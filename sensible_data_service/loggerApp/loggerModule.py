import pymongo
from utils.log_database import LogDatabase
import json
from utils import log_config as CONFIG
from Crypto.Hash import SHA512
import helperModule
import PERMISSIONS
import time
import datetime
import methods

class Logger(object):

	logDatabase = None

	def __init__(self):
		self.logDatabase = LogDatabase()

# In this case, Y is NOT the hash of the current D0 with the previous link, but a random seed.
# D0 is useless, added to make a consistent entry in the log, not used for authentication.
	def cryptoSetup(self): # make an overloaded method used also by the normal creation, for the "D payload"
#            self.logDatabase.writeEntry(CONFIG.FIRST_ENTRY, CONFIG.D0, helperModule.computeChecksum([CONFIG.D0]) , CONFIG.SEED) # Write the first [dummy] entry in the log + the authentication key [before being overridden]

                self.logDatabase.writeEntryWithMAC(CONFIG.FIRST_ENTRY, CONFIG.D0, helperModule.computeChecksum([CONFIG.D0]) , CONFIG.Y0, CONFIG.A0)

# log_entry = <flowID, D, C, Y>
# D = <userID,appID,payload>
	def append_dataflow(self, data):
		current_flowID = self.logDatabase.getMaxFlowID() + 1		
		current_D = helperModule.create_D(data)
		current_V = helperModule.create_V(current_D)
		previous_Y = self.logDatabase.getEntry(current_flowID - 1).get("Y")
		current_Y = helperModule.create_Y(previous_Y, current_V)
#		mongo_id_string = self.logDatabase.writeEntry(current_flowID, current_D, current_V, current_Y)	# Finally, writes the log entry


                previous_A = self.logDatabase.getEntry(current_flowID - 1).get("A")



                current_A = helperModule.update_A(previous_A)



                mongo_id_string = self.logDatabase.writeEntryWithMAC(current_flowID, current_D, current_V, current_Y, current_A)
                tuple_to_return = (current_flowID, mongo_id_string)
                return tuple_to_return


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

	    def __iter__(self): # Return the match method once, then stop
		yield self.match
		raise StopIteration
		    
	    def match(self, *args):         # Indicate whether or not to enter a case suite
		if self.fall or not args:
		    return True
		elif self.value in args:
		    self.fall = True
		    return True
		else:
		    return False

	def append(self, role, method, data):
		print
                returned = None
		st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') # Format : "2013-06-08 12:01:15"
		if (self.dispatching(role, method)): # If the check went fine
			print st + " ==> role = <" + role + "> has permission for method = <" + method + ">" # "2013-06-08 12:07:11 ==> user"
			returned = getattr(self, method)(data) # the corresponding method gets called with data as input
			if not method:
			    raise Exception("Method %s not implemented" % method_name)
		else:
			print st + " ==> role = <" + role + "> has NO permission for method = <" + method + ">" 
                return returned


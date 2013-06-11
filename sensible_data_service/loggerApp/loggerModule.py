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
            self.logDatabase.writeEntryWith_Z(CONFIG.FIRST_ENTRY, CONFIG.D0, CONFIG.V0, CONFIG.Z0)
            # TODO: do I need to update A here?

# log_entry = <flowID, D, C, Y>
# D = <userID,appID,payload>
	def append_dataflow(self, data):
                print "LOGGER APPEND"
		current_flowID = self.logDatabase.getMaxFlowID() + 1		
		current_D = helperModule.create_D(data)
		current_V = helperModule.create_V(current_D)

                previous_A = helperModule.read_A()

                previous_Z = self.logDatabase.getPrevious(current_flowID).get("Z")
                current_Z = helperModule.create_Z(current_V, previous_Z, previous_A)

                print "for flowID = " + str(current_flowID)
                print "resulting current_Z is = " + current_Z

                helperModule.update_A() # previous_A is deleted

                mongo_id_string = self.logDatabase.writeEntryWith_Z(current_flowID, current_D, current_V, current_Z) # Finally, writes the log entry
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


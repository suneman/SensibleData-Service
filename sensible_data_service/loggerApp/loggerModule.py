import pymongo
from utils.log_database import LogDatabase
import json
from utils import log_config as CONFIG
from Crypto.Hash import HMAC
from Crypto.Hash import SHA512
import helperModule

class Logger(object):

	logDatabase = None

	Dj = None
	Yj = None
	Yj_1 = None
	Zj = None
	Zj_1 = None

# For test:
	userID = ""
	initialUserAppflowID = 0


	def __init__(self):
		self.logDatabase = LogDatabase()
		self.cryptoSetup()		


# In this case, Y is NOT the hash of the current D0 with the previous link, but a random seed.
# D0 is useless, added to make a consistent entry in the log, not used for authentication.
# Z0 is the HashMAC of SEED. This is the farest link that chan be checked in the chain. If HMAC_A0(SEED) == myValue, ok.
	def cryptoSetup(self): # make an overloaded method used also by the normal creation, for the "D payload"
		h = HMAC.new(key=CONFIG.A0, msg=CONFIG.SEED,digestmod=SHA512) # Load the HMAC with the secret key A0, want to hash SEED, hash algo = SHA512
		self.Z0 = h.hexdigest().encode("utf-8") # The result is stored in Z = HMAC of SEED with the key A0 ==> Z=HMAC_A0_(SEED)
		C = helperModule.computeChecksum([CONFIG.D0])
		D = {"payload" : CONFIG.D0['payload'], "userID" : self.userID, "userAppFlow" : str(self.initialUserAppflowID), "appID" : CONFIG.D0['appID']} # Creates D for the first dummy entry
		self.logDatabase.writeEntry(0, D, C, CONFIG.SEED) # Write the first [dummy] entry in the log + the authentication key [before being overridden]


# data = <userID,appID,payload>
# Make the fileds dynamically read from the config file instead of hardcoded.
	def createDforlog(self, data):
		userID = data['userID']
		appID = data['appID']
		payload = data['payload']
		userAppFlow = self.logDatabase.getMaxUserAppFlow(userID, appID)
		return {"userID" : userID, "userAppFlow" : userAppFlow, "appID" : appID, "payload" : payload}


# Entry = <flowID, D, current_C, current_Y>
	def append(self, data):
		flowID = self.logDatabase.getMaxFlowID() + 1		
		D = self.createDforlog(data)
		current_C = helperModule.createC(D)
		previous_Y = self.logDatabase.getEntry(flowID - 1).get("Y")
		current_Y = helperModule.computeY(previous_Y, current_C)
		self.logDatabase.writeEntry(flowID, D, current_C, current_Y)	# Finally, writes the log entry

import pymongo
from utils.log_database import LogDatabase
import json
from utils import log_config as CONFIG
from Crypto.Hash import HMAC
from Crypto.Hash import SHA512
import helperModule

class Logger(object):

	logDatabase = None


	def __init__(self):
		self.logDatabase = LogDatabase()

# In this case, Y is NOT the hash of the current D0 with the previous link, but a random seed.
# D0 is useless, added to make a consistent entry in the log, not used for authentication.
# Z0 is the HashMAC of SEED. This is the farest link that chan be checked in the chain. If HMAC_A0(SEED) == myValue, ok.
	def cryptoSetup(self): # make an overloaded method used also by the normal creation, for the "D payload"
		h = HMAC.new(key=CONFIG.A0, msg=CONFIG.SEED,digestmod=SHA512) # Load the HMAC with the secret key A0, want to hash SEED, hash algo = SHA512
		C = helperModule.computeChecksum([CONFIG.D0])
		self.logDatabase.writeEntry(CONFIG.FIRST_ENTRY, CONFIG.D0, C, CONFIG.SEED) # Write the first [dummy] entry in the log + the authentication key [before being overridden]
# TODO: change the first Y, not seed but a HASH of C.



# log_entry = <flowID, D, C, Y>
# D = <userID,appID,payload>
	def append(self, data):
		flowID = self.logDatabase.getMaxFlowID() + 1		
		D = helperModule.createD(data)
		current_C = helperModule.createC(D)
		previous_Y = self.logDatabase.getEntry(flowID - 1).get("Y")
		current_Y = helperModule.computeY(previous_Y, current_C)
		self.logDatabase.writeEntry(flowID, D, current_C, current_Y)	# Finally, writes the log entry
		return flowID

	def getMaxFlowID(self):
		return self.logDatabase.getMaxFlowID()

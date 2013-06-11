from Crypto.Hash import SHA512
from Crypto.Hash import HMAC
import os
from utils import log_config as CONFIG

def convert(input):
	if isinstance(input, dict):
		return {convert(key): convert(value) for key, value in input.iteritems()}
	elif isinstance(input, list):
		return [convert(element) for element in input]
	elif isinstance(input, unicode):
		return input.encode('utf-8')
	else:
		return input


def extract(myDict, myList):
	if myDict is None:
		return
	for value in myDict.values():
		if isinstance(value, dict):
		    extract(value, myList)
		else:
		    myList.append(value)


# Computes the checsum of values only, so key order does not matter
#def computeChecksum(inputData):
#	h = SHA512.new()		
#	for item in inputData:
#		h.update(str(item))
#	checksum = h.hexdigest()
#	return checksum

def create_V(D):
	outputList = []
	extract(D,outputList)
	resultList = convert(outputList)
	resultList.sort() # sort the values, done so when later it will be checked, the hashes will be the same
        return ''.join(resultList) # from list to string


def create_D(data):
	userID = data['userID']
	appID = data['appID']
	payload = data['payload']
	return {"userID" : userID, "appID" : appID, "payload" : payload}

def create_Z(current_V, previous_Z, previous_A):
    hmac = HMAC.new(previous_A)
    hmac.update(current_V)
    hmac.update(previous_Z)
    return hmac.hexdigest()

def read_A():
    fr = open(CONFIG.FILE_A, 'r')
    A = fr.read()
    fr.close()
    return A

def update_A():
    A = read_A()
    print "before = " + A
#    calculated_A = calculateHash_A(1,A) # 1 round only
    calculated_A = A

    fw = open(CONFIG.FILE_A_TEMP, 'w')

    fw.write(calculated_A)
    fw.close()
    os.rename(CONFIG.FILE_A_TEMP, CONFIG.FILE_A)
    print "after = " + calculated_A
    return calculated_A

def calculateHash_A(rounds, A):
    print "rounds = " + str(rounds)
    print "A = " + A
    h = SHA512.new() # here or inside the loop?
    h.update(A)
    new_A = h.hexdigest()
    print "updated_A = " + new_A
    return new_A

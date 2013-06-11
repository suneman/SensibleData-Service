from Crypto.Hash import SHA512
from Crypto.Hash import HMAC

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
def computeChecksum(inputData):
	h = SHA512.new()		
	for item in inputData:
		h.update(str(item))
	checksum = h.hexdigest()
	return checksum


#def create_Y(previous_Y, current_V):
#	if (previous_Y is None or current_V is None):
#		print "Error: previous_Y or current_V = None. Exit"
#		exit(-1)
#	h = SHA512.new()
#	h.update(previous_Y)
#	h.update(current_V)
#	Y = h.hexdigest()
#	return Y	


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

def update_A(old_A):
    return computeChecksum(old_A)

def create_Z(current_V, previous_Z, current_A):
    hmac = HMAC.new(str(current_A))
    hmac.update(current_V)
    hmac.update(previous_Z)
    return hmac.hexdigest()

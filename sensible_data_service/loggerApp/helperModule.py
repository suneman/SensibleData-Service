from Crypto.Hash import HMAC
from Crypto.Hash import SHA512

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


def computeChecksum(inputData):
	h = SHA512.new()		
	for item in inputData:
		h.update(str(item))
	checksum = h.hexdigest()
	return checksum


def computeY(previous_Y, current_C):
	if (previous_Y is None or current_C is None):
		print "Error: previous_Y or current_C = None. Exit"
		exit(-1)
	h = SHA512.new()
	h.update(previous_Y)
	h.update(current_C) #only the checksum
	Y = h.hexdigest()
	return Y	


# Computes the checsum of the values, so key order does not matter
def createC(D):
	outputList = []
	extract(D,outputList)
	resultList = convert(outputList)
	resultList.sort()
	temp_C = computeChecksum(resultList)
	return temp_C


def createD(data):
	userID = data['userID']
	appID = data['appID']
	payload = data['payload']
	return {"userID" : userID, "appID" : appID, "payload" : payload}


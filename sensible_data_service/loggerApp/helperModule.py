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
    A = fr.read().encode("utf-8").strip(' \t\n\r') # ARGH!
    fr.close()
    return A

def update_A():
    A = read_A()
    calculated_A = calculateHash_A(1,A)
    fw = open(CONFIG.FILE_A_TEMP, 'w')
    fw.write(calculated_A)
    fw.close()
    os.rename(CONFIG.FILE_A_TEMP, CONFIG.FILE_A)
    return calculated_A

def calculateHash_A(rounds, A):
    for i in range(0,rounds):
        h = SHA512.new() # Inside the loop
        h.update(A)
        A = h.hexdigest()
    return A

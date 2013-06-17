from Crypto.Hash import SHA512
from Crypto.Hash import HMAC
import os
from utils import log_config as CONFIG
from Crypto import Random
from Crypto.PublicKey import RSA

import string
import random
import time
import datetime

from django.contrib.auth.models import User

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


def create_D(username, data):
    appID = data['appID']
    payload = data['payload']
    return {"userID" : username, "appID" : appID, "payload" : payload}

def create_Z(current_V, previous_Z, previous_A):
    hmac = HMAC.new(previous_A)
    hmac.update(current_V)
    hmac.update(previous_Z)
    return hmac.hexdigest()


def calculateHash_A(rounds, A): # TODO: This should be changed from SHA512 [fast] to bcrypt [slow] which is good for storing passwords
    for i in range(0,rounds):
        h = SHA512.new()
        h.update(A)
        A = h.hexdigest()
    return str(A)


def getTimestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') # Format : "2013-06-08 12:01:15" TODO: make it fine-grained. ms?


def permissionCheck(_request, _permission):
    if _request.user.is_authenticated():
        auth = True
    else:
        print "User NOT authenticated"
        auth = False

    if _request.user.has_perm(_permission):
        perm = True
    else:
        print "he has NO permissions"
        perm = False
    return (auth and perm) 


def isSuperUser(_request):
    superUser = _request.user.is_superuser # Only superusers can create this stuff. TODO: Tomorrow, add role "studyAdmin" and give him the permissioon for this task
    if not superUser:
        print "Not a superuser"
        return False
    return superUser


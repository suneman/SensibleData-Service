from loggerApp import loggerModule
from loggerApp import checkerModule
from django.http import HttpResponse
from loggerApp import PERMISSIONS
from loggerApp.signals import write_to_log
from utils import log_config as CONFIG


def setup():
    logger = loggerModule.Logger()
    if (logger.logDatabase.getMaxFlowID() == 0):
        logger.cryptoSetup()
    returned = logger.addUserKey("riccardo", CONFIG.A0)
#TODO: add keySetup
    return returned


def insert(request):
    logger = loggerModule.Logger()
    fakeJson = {"appID": "FUNF", "payload": "FUNF_dummyPayload", "userID": "FUNF_riccardo"}
#    returned_tuple = logger.append(PERMISSIONS.USER_ID, PERMISSIONS.DATAFLOW_ID, fakeJson)
    returned_tuple = logger.append(PERMISSIONS.USER_ID, "riccardo", PERMISSIONS.DATAFLOW_ID, fakeJson)
    return HttpResponse("inserted entry, flowID = " + str(returned_tuple[0]) + ", mongo_id = " + returned_tuple[1])


def check(request):
    checker = checkerModule.Checker()
    audit = checker.check_Z()
    returned = write_to_log.send(sender=None, user=request.user) 
    return HttpResponse("last check = " + str(audit))


def reset(request):
    logger = loggerModule.Logger()
    logger.logDatabase.reset()
    logger.keystore.reset()
    key = setup()
    return HttpResponse("reset done")

from loggerApp import loggerModule
from loggerApp import checkerModule
from django.http import HttpResponse
from loggerApp import PERMISSIONS

def insert(request):
	logger = loggerModule.Logger()
	if (logger.logDatabase.getMaxFlowID() == 0):
		logger.cryptoSetup()
	fakeJson = {"appID": "FUNF", "payload": "FUNF_dummyPayload", "userID": "FUNF_riccardo"}
	returned_tuple = logger.append(PERMISSIONS.USER_ID, PERMISSIONS.DATAFLOW_ID, fakeJson)
	return HttpResponse("inserted entry, flowID = " + str(returned_tuple[0]) + ", mongo_id = " + returned_tuple[1])


def check(request):
	checker = checkerModule.Checker()
	audit = checker.check()
	return HttpResponse("last check = " + str(audit))

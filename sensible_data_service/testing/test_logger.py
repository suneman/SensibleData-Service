from loggerApp import loggerModule
from loggerApp import checkerModule
from django.http import HttpResponse

def insert(request):

	fakeJson = {"appID": "fb", "payload": "dummyPayload", "userAppID": 1, "userID": "riccardo"}

	logger = loggerModule.Logger()
	logger.append(fakeJson)
	return HttpResponse("insert")


def check(request):
	checker = checkerModule.Checker()
	checker.check()
	return HttpResponse("check")

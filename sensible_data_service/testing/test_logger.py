from logger_manager import logger_manager
from django.http import HttpResponse

def testIt(request):

	fakeJson = {"appID": "fb", "payload": "dummyPayload", "userAppID": 1, "userID": "riccardo"}

	logger = logger_manager.Logger()
	logger.append(fakeJson)
	return HttpResponse("CIAO")

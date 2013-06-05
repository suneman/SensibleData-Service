from logger_manager import logger_manager
from django.http import HttpResponse

def testIt(request):
	logger = logger_manager.Logger()
	return HttpResponse("CIAO")

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from authorization_manager.authorization_manager import *
import bson.json_util as json
from connector_pipes.connector_pipe_funf import connector_pipe_funf
<<<<<<< HEAD

def testing(request):
	response = 'dupa'
=======
from application_manager.application_manager import ApplicationManager
from logger import Logger

def testing(request):
	authorizationManager = AuthorizationManager()


	user = 'arek'
	pipe = 'connector_funf'
	scope = 'input'
	params = {'token':'cde'}

	#authorizationManager.insertAuthorization(user, pipe, scope, params)
	#response = {'hello':'world'}

	pipe = connector_pipe_funf.ConnectorFunfPipe()

	applicationManager = ApplicationManager()
	response = applicationManager.registerApplication(name='krowa', owner='john', connector='connector_funf', scopes='all_probes', description="this is an awesome app", params={})

	#response = pipe.getAuthorization('aaaa')



	logger = Logger()

>>>>>>> a405c633d19c8084766a0a05cc973aec83f2e101
	return HttpResponse(json.dumps(response))


import authorization_manager
from authorization_manager import gcm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from application_manager.models import Application, GcmRegistration, Device
from authorization_manager.models import Authorization
from oauth2app.models import Client, AccessToken
from django.shortcuts import redirect
import uuid
import hashlib

@login_required
def grant(request):

        user = request.user
	try: scope = request.REQUEST.get('scope').split(',')
	except AttributeError: return HttpResponse(json.dumps({"error":"no scope provided"}))
        client_id = request.REQUEST.get('client_id', '')
        device_id = request.REQUEST.get('device_id', '')
        gcm_id = request.REQUEST.get('gcm_id', '')


	#TODO: device support
	try:
		gcm_registration = GcmRegistration.objects.get(user=user, device_id=device_id, application=Application.objects.get(client=Client.objects.get(key=client_id)))
	except: gcm_registration = None


	if gcm_id == '' and gcm_registration == None:
		#we cannot start authorization, we don't know the gcm id
		return HttpResponse(json.dumps({'error':'please start registration from your phone'}))

	if gcm_id != '' and device_id != None and gcm_registration != None:
		#we should update gcm_id
		gcm_registration.gcm_id = gcm_id
		gcm_registration.device_id = gcm_id
		gcm_registration.save()

	#TODO: create new gcm registration
	#TODO: veriy params
	#TODO: check scopes that are allowed for this app

	redirect_uri = '/authorization_manager/oauth2/authorize/?'
	redirect_uri += 'client_id='+client_id
	redirect_uri += '&response_type=token'
	redirect_uri += '&scope='+','.join(scope)
	redirect_uri += '&redirect_uri='+Client.objects.get(key=client_id).redirect_uri

	return redirect(redirect_uri)

@login_required
def granted(request):
        #TODO: push the token to the phone over GCM
        #TODO: get confirmation
        #TODO: redirect user back to platform

	access_token = AccessToken.objects.get(token=request.REQUEST.get('access_token'))

	server_nonce = hashlib.sha256(str(uuid.uuid4())).hexdigest() #we do it here not in the model, so all authorizations from this batch have the same nonce
	t= ''
	for scope in access_token.scope.all():
		authorization = Authorization.objects.create(user=access_token.user, scope=scope, application=Application.objects.get(client=access_token.client), access_token=access_token, nonce=server_nonce)

	#to user, application, device, parameters, nonce
	gcm.sendAuthorization()

        return HttpResponse('authorization granted '+access_token.token+' '+t)

@login_required
def revoke(request):

        #TODO: remove scopes from the authorization

        return HttpResponse(request.user)

@login_required
def sync(request):

        #TODO: make the authorizations reflect the submit parameters

        return HttpResponse(request.user)

def confirm(request):
	return HttpResponse('confirmed')

def buildUri(connector, application):
        grant_uri = connector.grant_url+'?'
        revoke_uri = connector.revoke_url+'?'
        for param in application.params.all():
                if param.key == 'client_id':
                        grant_uri += 'client_id='+param.value+'&'
                        revoke_uri += 'client_id='+param.value+'&'
        grant_uri += 'scope=_scope_'
        revoke_uri += 'scope=_scope_'

        #TODO: add message for the empty uris, when the action needs to be initiated from somewhere else
        return {'grant_uri':grant_uri, 'revoke_uri': revoke_uri}

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^redirect_uri/?$', 'platform_manager.registration.callback'),
	url(r'^discover/?$', 'platform_manager.discover.init'),
	url(r'^userStatus/?$', 'platform_manager.user_status.userStatus'),
	url(r'^serviceAuthorizations/?$', 'platform_manager.service_authorizations.serviceAuthorizations'),
)

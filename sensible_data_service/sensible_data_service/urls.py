from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^connectors/', include('connectors.urls')),
	url(r'^authorization_manager/', include('authorization_manager.urls')),
	#url(r'^application_manager/', include('application_manager.urls')), #used via django admin atm
	url(r'^platform_api/', include('platform_manager.urls')),
	url(r'^openid/', include('django_openid_auth.urls')),
	url(r'^admin/', include(admin.site.urls)),
	 
	url(r'^test/', include('testing.urls')),
)

from django.conf.urls import patterns, include, url
from loggerApp import views
from loggerApp import loggerModule

urlpatterns = patterns('',
        url(r'^$', views.index, name="index"),
        
        url(r'^create_new_user', "loggerApp.loggerModule.createNewUser"),
        url(r'^append', "loggerApp.loggerModule.append"),
        url(r'^check', "loggerApp.loggerModule.check"),

#        url(r'^test', "loggerApp.loggerModule.test"),
)

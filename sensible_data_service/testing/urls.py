from django.conf.urls import patterns, include, url
from testing import views
from testing import test_logger

urlpatterns = patterns('',
#        url(r'^$', test_logger.testIt),
        url(r'^insert/', test_logger.insert),
        url(r'^check/', test_logger.check),
)

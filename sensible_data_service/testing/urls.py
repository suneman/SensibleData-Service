from django.conf.urls import patterns, include, url
from testing import test_logger

urlpatterns = patterns('',
        url(r'^insert/', test_logger.insert),
        url(r'^check/', test_logger.check),
        url(r'^reset/', test_logger.reset),
)

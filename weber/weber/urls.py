from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from myapp import views
from home_func.views import SSE
from login import views
import socketio.sdjango
socketio.sdjango.autodiscover()

urlpatterns = patterns('',
    url(r'^theweber.in/', include('login.urls')),
    url(r'^theweber.in/', include('home_func.urls')),
    
    #url(r'^sse_push_message/$', 'home_func.views.sse_push_message'),
)
urlpatterns += staticfiles_urlpatterns()
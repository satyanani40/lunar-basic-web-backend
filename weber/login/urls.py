from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weber.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$',TemplateView.as_view(template_name='index.html')),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/theweber.in/'}),
    url(r'^index$',TemplateView.as_view(template_name='index.html')),
    url(r'^header$',TemplateView.as_view(template_name='header.html')),

    url(r'^home$',TemplateView.as_view(template_name='home.html')),
    url(r'^login_check','login.views.login_check'),
    url(r'^register$','login.views.register'),
    url(r'^login$',TemplateView.as_view(template_name='login.html')),
    #url(r'^home$','login.views.home'),
    #url(r'^logout$','login.views.logout_view'),

)

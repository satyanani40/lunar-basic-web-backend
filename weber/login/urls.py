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

    #surya urls
    url(r'^activate/(?P<email>[\d+\w@\w.\wa-z\wA-Z\w1-9\w:\w;\w_\w=\w{}]+)/$', 'login.views.email_confirmation'),
    url(r'^confirm_registration', TemplateView.as_view(template_name='confirm_registration.html')),
    url(r'^forgot_password', TemplateView.as_view(template_name='forgotpassword.html')),
    url(r'^set_new_password', TemplateView.as_view(template_name='setpassword.html')),
    url(r'^password_recovery', 'login.views.password_recovery'),
    url(r'^password_reset_success', 'login.views.password_reset_success'),
    url(r'^set_password/(?P<password_email>[\d+\w@\w.\wa-z\wA-Z\w1-9\w:\w;\w_\w=\w{}]+)/$', 'login.views.set_password'),
    url(r'^invite_friends', TemplateView.as_view(template_name='invitefriends.html')),
    url(r'^send_invitation', 'login.views.send_invitation'),





)

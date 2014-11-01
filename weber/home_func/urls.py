from django.conf.urls import patterns, include, url
from home_func.views import *
from django.views.generic import TemplateView

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'weber.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^profile/(?P<username>[-\w]+)/$',TemplateView.as_view(template_name='profile.html')),
    url(r'^get_profile_info/(?P<username>[-\w]+)/$','home_func.views.get_profile_info'),
    url(r'^sse/$', SSE.as_view()),
    url(r'^post_status$','home_func.views.post_status'),
    url(r'^load_more_posts','home_func.views.load_scroll_posts'),
    url(r'^search','home_func.views.search_titles'),
    url(r'^updateinfo','home_func.views.update_userinfo'),
    url(r'^addfriend','home_func.views.add_friend'),
    url(r'^cancel_request','home_func.views.cancelrequest'),
    url(r'^updateinfo','home_func.views.update_info'),
    url(r'^deletepost','home_func.views.delete_post'),
    url(r'^loaded_userposts','home_func.views.loaded_userposts'),
    url(r'^savepost','home_func.views.savepost'),

    url(r'^upload_profile_pic','home_func.views.upload_profile_pic'),
    url(r'^get_userpic','home_func.views.get_userpic'),

    url(r'^frnd_notifications','home_func.views.frnd_notifications'),
    url(r'^accept_friend','home_func.views.accept_friend'),
    url(r'^change_password','home_func.views.change_password'),
    url(r'^block_person','home_func.views.block_selected_person'),
    url(r'^unblock_person','home_func.views.unblock_selected_person'),


)

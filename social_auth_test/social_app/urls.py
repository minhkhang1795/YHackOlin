from django.conf.urls import url
from django.contrib.auth.views import logout

from social_auth_test import settings
from . import views

app_name = 'social_app'

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_URL}, name='logout'),
    url(r'^trending/$', views.post_listing, name='post_list_view'),
    url(r'^home/$', views.home, name='post_list_view'),
    url(r'^(?P<post_id>[0-9]+)/$', views.post_details, name='post_details'),
    url(r'^(?P<post_id>[0-9]+)/edit/$', views.post_editing, name='post_editing'),

    url(r'^like-post/$', views.like_count, name='like_count'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()

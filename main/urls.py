from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<token>[a-z0-9]{10})/$', views.receiver, name='receiver'),
    url(r'^logout/?$', views.logout_user, name='logout'),
    url(r'^about/?$', views.about, name='about'),
]

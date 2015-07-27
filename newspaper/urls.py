from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_login, name='login'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^index/$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^favorites/$', views.favorites, name='favorites'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^logout/$', views.user_logout, name='logout'),
]

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^accounts/login', auth_views.login, {'template_name': 'registeration/login.html'},name="login"),
    url(r'^accounts/register/', views.registerPage),
    url(r'^accounts/logout/$', auth_views.logout, name="logout"),

    url(r'^$', views.home, name='index'),
    url(r'profile', views.profilePage, name='profile'),
    url(r'prof/new', views.profileEdit, name='profileedit'),
    url(r'job/list', views.joblistPage, name='joblist'),
    url(r'job/newform', views.jobpostPage, name='jobpost'),
    url(r'job/new', views.jobNewPost, name='newjobpost'),
    url(r'job/request', views.requestJob, name='requestjob'),
    url(r'job/reqprocess', views.requestJobProcess, name='requestjobprocess'),
    url(r'about', views.about, name='about')
]
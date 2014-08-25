from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from blogging import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"),
    url(r'^accounts/register/$', views.RegisterUser.as_view()),
    url(r'^accounts/register_success/$', 'blogging.views.register_success'),
    url(r'^accounts/login/$', 'blogging.views.login'),
    url(r'^accounts/auth/$', 'blogging.views.auth_view'),
    #url(r'^accounts/logout/$', 'blogging.views.logout'),
    url(r'^accounts/logout/$', views.logout.as_view()),
   # url(r'^accounts/loggedin/$', TemplateView.as_view(template_name='loggedin.html'), name="valid_login"),
   # url(r'^accounts/invalid/$', TemplateView.as_view(template_name='invalid_valid.html'), name="invalid_login"),
   url(r'^accounts/loggedin/$', views.loggedin.as_view()),
   url(r'^accounts/invalid/$', views.invalid_login.as_view()),
)

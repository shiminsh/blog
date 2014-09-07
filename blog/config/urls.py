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
    url(r'^accounts/login/$', 'blogging.views.login', name="login"),
    url(r'^accounts/logout/$', views.Logout.as_view()),
    url(r'^newpost/$', 'blogging.views.createblog'),
    url(r'^posted/$', views.PostByMe.as_view()),
    url(
    regex=r'^accounts/loggedin/$',
    view=views.UserListView.as_view(),
    name='detail'
    ),
)
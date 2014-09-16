from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from blogging import views
from django.contrib.auth.decorators import user_passes_test
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name="home"),
    url(r'^accounts/register/$',user_passes_test(lambda user: user.is_anonymous(), '/accounts/loggedin/', None)(views.RegisterUser.as_view())),
    url(r'^accounts/login/$', user_passes_test(lambda user: user.is_anonymous(), '/accounts/loggedin/', None)(views.LoginView.as_view())),
    url(r'^accounts/logout/$', views.Logout.as_view()),
    url(r'^posted/$', views.PostByMe.as_view()),
    url(
    regex=r'^accounts/loggedin/$',
    view=views.UserListView.as_view(),
    name='detail'
    ),
    url(
        regex=r'^blog/(?P<pk>[\w\-_]+)/$',
        view=views.UserDetailView.as_view(),
        name='user_detail'
    ),
    url(
        regex=r'^update/(?P<pk>[\w\-_]+)/edit/$',
        view= views.UserUpdate.as_view(),
        name='user-update'
    ),

)
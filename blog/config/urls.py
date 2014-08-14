from django.conf.urls import patterns, include, url
from blogging import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/register/$', views.RegisterUser.as_view()),
    url(r'^accounts/register_success/$', 'blogging.views.register_success'),
)

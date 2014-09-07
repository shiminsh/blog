from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import auth
from blogging.forms import RegistrationForm, LoginForm, BlogForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic import DetailView, ListView
from blogging.models import Blog


class RegisterUser(FormView):
     template_name='register.html'
     form_class=RegistrationForm
     success_url='/accounts/login'

     def form_valid(self, form):
        form.save()
        return super(RegisterUser, self).form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/accounts/loggedin/'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

login = LoginView.as_view()


class Loggedin(TemplateView):
    template_name='loggedin.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
         return super(Loggedin, self).dispatch(*args, **kwargs)


class Logout(TemplateView):
    template_name='logout.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(Logout, self).get(self.request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Logout, self).dispatch(*args, **kwargs)

def createblog(request):
    return render_to_response('newpost.html', context_instance=RequestContext(request))


def postbyme(request):
    title=request.POST.get('title', '')
    description=request.POST.get('description', '')
    d=Blog(title=title.lower(), description=description.lower())
    d.user = request.user
    d.save()
    return HttpResponseRedirect('/accounts/loggedin/')

class PostByMe(FormView):
    form_class=BlogForm
    success_url='/accounts/loggedin/'
    template_name='newpost.html'

    def form_valid(self, form):
        blog=form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        return super(PostByMe, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostByMe, self).dispatch(*args, **kwargs)


class UserListView(ListView):
    model = Blog
    template_name = 'loggedin.html'

    def get_queryset(self):
        return self.request.user.blog_set.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)


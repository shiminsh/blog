from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib import auth
from blogging.forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class RegisterUser(FormView):
     template_name='register.html'
     form_class=RegistrationForm
     success_url='/accounts/login'

     def form_valid(self, form):
        form.save()
        return super(RegisterUser, self).form_valid(form)

def register_success(request):
    return render_to_response('register_success.html')


# def login(request):
#    c = {}
#    c.update(csrf(request))
#    c['form'] = LoginForm()
#    return render_to_response('login.html', c)

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/accounts/loggedin/'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


login = LoginView.as_view()
        

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')

class loggedin(TemplateView):
    template_name='loggedin.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
         return super(loggedin, self).dispatch(*args, **kwargs)


class invalid_login(TemplateView):
    template_name='invalid_login.html'


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(logout, self).dispatch(*args, **kwargs)


class logout(TemplateView):
    template_name='logout.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(logout, self).get(self.request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(logout, self).dispatch(*args, **kwargs)
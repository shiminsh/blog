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
from django.contrib import messages
from django.views.generic import UpdateView



class RegisterUser(FormView):
     template_name='register.html'
     form_class=RegistrationForm
     success_url='/accounts/register'

     def form_valid(self, form):
        form.save()
        return super(RegisterUser, self).form_valid(form)



class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/accounts/loggedin/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(self.request, user)
        else:
            messages.warning(self.request, 'Login Credentials does not exists.')
        return super(LoginView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs



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
    success_url='/blog/{{ blog.id }}/'

    def get_queryset(self):
        return self.request.user.blog_set.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

class UserDetailView(DetailView):
    template_name = 'blog.html'
    model = Blog

    def get_object(self, queryset=None):
    # Use a custom queryset if provided; this is required for subclasses
    # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)
        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})
        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                             "either an object pk or a slug."
                             % self.__class__.__name__)
        return self.request.user.blog_set.get(id=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserDetailView, self).dispatch(*args, **kwargs)

class UserUpdate(UpdateView):  
    form_class = BlogForm
    template_name = 'update.html'
    model = Blog

    def get_success_url(self):
        self.success_url = '/accounts/loggedin/'
        return self.success_url

        #get object
    def get_object(self, queryset=None): 
        return self.request.user.blog_set.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['blog_id'] = self.kwargs['pk']
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserUpdate, self).dispatch(*args, **kwargs)

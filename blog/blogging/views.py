from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.views.generic import FormView
from blogging.forms import RegistrationForm


class RegisterUser(FormView):
     template_name='register.html'
     form_class=RegistrationForm
     success_url='/accounts/register_success'

     def form_valid(self, form):
        form.save()
        return super(RegisterUser, self).form_valid(form)

def register_success(request):
    return render_to_response('register_success.html')


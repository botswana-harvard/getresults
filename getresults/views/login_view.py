from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic.edit import FormView
from getresults.forms import LoginForm
from django.utils.decorators import method_decorator


class LoginView(FormView):
    """A create view for Foo model"""
    template_name = "login.html"
    form_class = LoginForm
    success_url = '/home/'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})

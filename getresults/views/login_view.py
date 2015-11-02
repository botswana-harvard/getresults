from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login

from django.views.generic.edit import FormView
from getresults.forms import LoginForm
from django.utils.decorators import method_decorator
from braces.views import FormInvalidMessageMixin


class LoginView(FormInvalidMessageMixin, FormView):
    """A create view for Foo model"""
    template_name = "login.html"
    form_class = LoginForm
    success_url = '/home/'
    form_invalid_message = 'Invalid username or password.'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next', self.success_url)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'))
        if user:
            if user.is_active:
                login(self.request, user)
                return super(FormView, self).form_valid(form)
        return self.form_invalid(form)

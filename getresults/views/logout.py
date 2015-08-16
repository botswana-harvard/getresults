from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_url'))

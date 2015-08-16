from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


@csrf_protect
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            login(request, user)
            if request.POST.get('next') != '':
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse('home'))
    else:
        template = 'login.html'
        return render_to_response(
            template,
            context_instance=RequestContext(request)
        )

"""xx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin
from getresults.admin import admin_site
from getresults.views import HomeView, LoginView, LogoutView
from getresults_result import urls as getresults_result_urls
from getresults_csv import urls as getresults_csv_urls

admin.autodiscover()

urlpatterns = [
    url(r'^admin/logout/', LogoutView.as_view(url='/login/')),
    url(r'^login/', LoginView.as_view(), name='login_url'),
    url(r'^logout/', LogoutView.as_view(url='/login/'), name='logout_url'),
    url(r'^admin/', include(admin_site.urls)),
    url(r'^accounts/login/', LoginView.as_view()),
    url(r'^home/', HomeView.as_view(), name='home'),
    url(r'^result/import/', include(getresults_csv_urls), name='import_url'),
    url(r'^result/', include(getresults_result_urls), name='result_url'),
    url(r'', HomeView.as_view(), name='default'),
]

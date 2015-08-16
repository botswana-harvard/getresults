from django.contrib.admin import AdminSite


class GetresultsAdminSite(AdminSite):

    site_header = 'Getresults administration'
    site_title = 'Getresults site admin'
    login_template = 'login.html'
    logout_template = 'login.html'
admin_site = GetresultsAdminSite(name='getresultsadmin')

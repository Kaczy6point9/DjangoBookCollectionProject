from django.shortcuts import render


def home(request):
    site_title = 'Login Site'
    template_name = 'home.html'
    context = {'title': site_title}
    return render(request, template_name, context)
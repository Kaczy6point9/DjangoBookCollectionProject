from django.shortcuts import render


def home(request):
    site_title = 'Login Site'
    return render(request, 'home.html', {'title': site_title})
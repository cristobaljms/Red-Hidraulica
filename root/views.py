from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def login(request):
    return render(request, 'pages/login.html')

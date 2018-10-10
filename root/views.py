from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#@login_required(login_url='/login/')
def index(request):
    return render(request, 'base.html')

def login(request):
    return render(request, 'pages/login.html')

@login_required(login_url='/login/')
def beneficiarios(request):
    return render(request, 'sections/beneficiarios/index.html')

@login_required(login_url='/login/')
def operativos(request):
    return render(request, 'sections/operativos/index.html')

@login_required(login_url='/login/')
def reportes(request):
    return render(request, 'sections/reportes/index.html')
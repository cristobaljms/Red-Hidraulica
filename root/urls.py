"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, login, beneficiarios, operativos, reportes
#from beneficiarios.views import BeneficiariosListView, BeneficiariosCreateView, BeneficiariosUpdateView, DeleteBeneficiario
from proyectos.views import ProyectosListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('proyectos/', ProyectosListView.as_view(), name='proyectos'),
    # path('beneficiarios/', BeneficiariosListView.as_view(), name='beneficiarios'),
    #path('beneficiarios/crear', BeneficiariosCreateView.as_view(), name='beneficiarios_crear'),
    #path('beneficiarios/editar/<int:pk>/', BeneficiariosUpdateView.as_view(), name='beneficiarios_editar'),
    #path('beneficiarios/eliminar/<int:pk>/', DeleteBeneficiario, name='beneficiarios_eliminar'),
    #path('operativos/', operativos, name='operativos'),
    #path('reportes/', reportes, name='reportes'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
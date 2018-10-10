from django.shortcuts import render
from .models import Proyecto
from django.views import generic

# Create your views here.
class ProyectosListView(generic.ListView):
    model = Proyecto
    template_name = 'sections/proyectos/index.html'  # Specify your own template name/location
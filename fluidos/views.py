from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from fluidos.models import Fluido
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import re

def DeleteFluidos(request, pk):
    Fluido.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# Create your views here.
class FluidosListView(generic.ListView):
    model = Fluido
    template_name = 'sections/fluidos/list.html' 

class FluidosCreateView(generic.CreateView):
    template_name = "sections/fluidos/create.html"

    def get(self, request, *args, **kwargs):
        context = { }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        descripcion = request.POST.get('descripcion')
        viscosidad_cinematica = request.POST.get('viscosidad_cinematica')
        valor_viscocidad = request.POST.get('valor_viscocidad')
        if len(descripcion) < 1:
            messages.add_message(request, messages.ERROR, 'El nombre del fluido debe ser mayor a 1 digito')
            return redirect('fluidos_crear')

        if not(re.match('\d', valor_viscocidad)):
            messages.add_message(request, messages.ERROR, 'El valor de la viscosidad es invalido, debe ser numerico')
            return redirect('fluidos_crear')

        f = Fluido(descripcion=descripcion, viscosidad_cinematica=viscosidad_cinematica,  valor_viscocidad=valor_viscocidad)
        f.save()
        
        messages.add_message(request, messages.SUCCESS, 'Fluido creado con exito')
        return redirect('fluidos')
        

class FluidosUpdateView(generic.View):
    template_name = "sections/fluidos/edit.html"

    def get(self, request, *args, **kwargs):
        fluido = Fluido.objects.get(pk=kwargs['pk'])
        context = {
            'fluido':fluido
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_fluido = request.POST.get('id')
        descripcion = request.POST.get('descripcion')
        viscosidad_cinematica = request.POST.get('viscosidad_cinematica')
        valor_viscocidad = request.POST.get('valor_viscocidad')

        try:
            f = Fluido.objects.get(pk=id_fluido)
        except Fluido.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No existe el fluido')
            return redirect('fluidos')

        if len(descripcion) < 1:
            messages.add_message(request, messages.ERROR, 'El nombre del fluido debe ser mayor a 1 digito')
            return redirect('fluidos_editar', pk=id_fluido)

        if not(re.match('\d', str(valor_viscocidad))):
            messages.add_message(request, messages.ERROR, 'El valor de la viscosidad es invalido, debe ser numerico')
            return redirect('fluidos_editar', pk=id_fluido)

        f.descripcion = descripcion
        f.viscosidad_cinematica = viscosidad_cinematica
        f.valor_viscocidad = valor_viscocidad
        f.save()
        
        messages.add_message(request, messages.SUCCESS, 'Fluido editado con exito')
        return redirect('fluidos')
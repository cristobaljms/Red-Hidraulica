from django.shortcuts import render
from .models import Material
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import re

# Create your views here.
class MaterialesListView(generic.ListView):
    model = Material
    template_name = 'sections/materiales/list.html'  # Specify your own template name/location


class MaterialesCreateView(generic.CreateView):
    template_name = "sections/materiales/create.html"

    def get(self, request, *args, **kwargs):
        context = { }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        descripcion = request.POST.get('descripcion')
        ks = request.POST.get('ks')

        if len(descripcion) < 1:
            messages.add_message(request, messages.ERROR, 'El nombre del material debe ser mayor a 1 digito')
            return redirect('materiales_crear')
            
        if not(re.match('\d', str(ks))):
            messages.add_message(request, messages.ERROR, 'ks invalido, debe ser numerico')
            return redirect('materiales_crear')

        m = Material(descripcion=descripcion, ks=ks)
        m.save()
        
        messages.add_message(request, messages.SUCCESS, 'Material creado con exito')
        return redirect('materiales')
        

class MaterialesUpdateView(generic.View):
    template_name = "sections/materiales/edit.html"

    def get(self, request, *args, **kwargs):
        material = Material.objects.get(pk=kwargs['pk'])
        context = {
            'material':material
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_material = request.POST.get('id')
        descripcion = request.POST.get('descripcion')
        ks = request.POST.get('ks')

        try:
            m = Material.objects.get(pk=id_material)
        except Material.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No existe el material')
            return redirect('materiales')

        if len(descripcion) < 1:
            messages.add_message(request, messages.ERROR, 'El nombre del material debe ser mayor a 1 digito')
            return redirect('materiales_editar', pk=id_material)

        if not(re.match('\d', str(ks))):
            messages.add_message(request, messages.ERROR, 'ks invalido, debe ser numerico')
            return redirect('materiales_editar', pk=id_material)

        m.descripcion = descripcion
        m.ks = ks
        m.save()
        
        messages.add_message(request, messages.SUCCESS, 'Material editado con exito')
        return redirect('materiales')


        
class MaterialesDeleteView(generic.DeleteView):
    template_name = "sections/materiales/delete.html"
    def get(self, request, *args, **kwargs):
        material = Material.objects.get(pk=kwargs['pk'])
        context = {
            'material': material
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        Material.objects.filter(pk=kwargs['pk']).delete()
        messages.add_message(request, messages.SUCCESS, 'Material eliminado')
        return redirect('materiales')
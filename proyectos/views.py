from django.shortcuts import render
from .models import Proyecto, Nodo, Tuberia, Reservorio
from materiales.models import Material
from fluidos.models import Fluido
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
import re
from django.http import JsonResponse
import json

class ProyectoAdminView(generic.CreateView):
    template_name = "sections/proyectos/show.html"

    def get(self, request, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=kwargs['pk'])
        nodos = Nodo.objects.filter(proyecto=proyecto)
        tuberias = Tuberia.objects.filter(proyecto=proyecto)
        reservorios = Reservorio.objects.filter(proyecto=proyecto)

        context = {
            'proyecto': proyecto,
            'nodos':nodos,
            'tuberias':tuberias,
            'reservorios': reservorios 
        }
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        tipo = request.POST.get('tipo')
        id_proyecto = request.POST.get('id_proyecto')

        if (tipo == 'nodo'):
            numero = request.POST.get('numero')
            demanda = request.POST.get('demanda')
            cota = request.POST.get('cota')
            if len(numero) > 4:
                messages.add_message(request, messages.ERROR, 'Nombre del nodo no puede ser mayor de 4 caracteres')
                return redirect('proyecto_administrar', id_proyecto)

            if not(re.match('\d', str(demanda))):
                messages.add_message(request, messages.ERROR, 'demanda invalida, debe ser numerico')
                return redirect('proyecto_administrar', id_proyecto)

            if not(re.match('\d', str(cota))):
                messages.add_message(request, messages.ERROR, 'cota invalida, debe ser numerico')
                return redirect('proyecto_administrar', id_proyecto)
            proyecto = Proyecto.objects.get(pk=id_proyecto)

            nodo = Nodo(proyecto=proyecto, numero=numero, cota=cota, demanda=demanda)
            nodo.save()
            messages.add_message(request, messages.SUCCESS, 'Nodo creado con exito')
            return redirect('proyecto_administrar', id_proyecto)
        elif (tipo == 'tuberia'):
            numero = request.POST.get('numero')
            longitud = request.POST.get('longitud')
            diametro = request.POST.get('diametro')
            start = request.POST.get('start')
            end = request.POST.get('end')

            if start == '0' or end == '0':
                messages.add_message(request, messages.ERROR, 'Debe ingresar el nodo incial y el nodo final')
                return redirect('proyecto_administrar', id_proyecto)

            if len(numero) > 4:
                messages.add_message(request, messages.ERROR, 'Nombre del nodo no puede ser mayor de 4 caracteres')
                return redirect('proyecto_administrar', id_proyecto)

            if not(re.match('\d', str(longitud))):
                messages.add_message(request, messages.ERROR, 'longitud invalida, debe ser numerico')
                return redirect('proyecto_administrar', id_proyecto)

            if not(re.match('\d', str(diametro))):
                messages.add_message(request, messages.ERROR, 'diametro invalido, debe ser numerico')
                return redirect('proyecto_administrar', id_proyecto)

            if start == end:
                messages.add_message(request, messages.ERROR, 'El nodo de inicio no puede ser igual al nodo final')
                return redirect('proyecto_administrar', id_proyecto)

            nstart = Nodo.objects.get(pk = start)  
            nend = Nodo.objects.get(pk = end)     
            proyecto = Proyecto.objects.get(pk=id_proyecto)
            tuberia = Tuberia(proyecto=proyecto, numero=numero, longitud=longitud, diametro=diametro, start=nstart.numero, end = nend.numero)
            tuberia.save()
            messages.add_message(request, messages.SUCCESS, 'Tuberia creada con exito')
            return redirect('proyecto_administrar', id_proyecto)
        else:
            numero = request.POST.get('numero')
            z = request.POST.get('z')
            if len(numero) > 4:
                messages.add_message(request, messages.ERROR, 'Nombre del reservorio no puede ser mayor de 4 caracteres')
                return redirect('proyecto_administrar', id_proyecto)
            
            if not(re.match('\d', str(z))):
                messages.add_message(request, messages.ERROR, 'z invalido, debe ser numerico')
                return redirect('proyecto_administrar', id_proyecto)
            
            proyecto = Proyecto.objects.get(pk=id_proyecto)
            reservorio = Reservorio(numero=numero, z=z, proyecto=proyecto)
            reservorio.save()
            messages.add_message(request, messages.SUCCESS, 'Reservorio creado con exito')
            return redirect('proyecto_administrar', id_proyecto)

class ProyectosListView(generic.ListView):
    model = Proyecto
    template_name = 'sections/proyectos/index.html'


class ProyectosCreateView(generic.CreateView):
    template_name = "sections/proyectos/create.html"

    def get(self, request, *args, **kwargs):
        fluidos = Fluido.objects.all()
        material = Material.objects.all()
        context = { 'fluidos':fluidos, 'material':material }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        fluido = request.POST.get('fluido')
        material = request.POST.get('material')

        if len(nombre) < 2:
            messages.add_message(request, messages.ERROR, 'El nombre del proyecto debe ser mayor a 2 digitos')
            return redirect('proyectos_crear')

        if fluido == '0':
            messages.add_message(request, messages.ERROR, 'El fluido no es valido')
            return redirect('proyectos_crear')
        
        if material == '0':
            messages.add_message(request, messages.ERROR, 'El material no es valido')
            return redirect('proyectos_crear')

        if Proyecto.objects.filter(nombre=nombre).exists():
            messages.add_message(request, messages.ERROR, 'Este nombre ya se encuentra registrado.')
            return render(request, self.template_name)
        else:
            f = Fluido.objects.get(pk=fluido)
            m = Material.objects.get(pk=material)
            p = Proyecto(nombre=nombre, fluido=f, material=m)
            p.save()
        
        messages.add_message(request, messages.SUCCESS, 'Proyecto creado con exito')
        return redirect('proyectos')
        

class ProyectosUpdateView(generic.View):
    template_name = "sections/proyectos/edit.html"

    def get(self, request, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=kwargs['pk'])
        fluidos = Fluido.objects.all()
        materiales = Material.objects.all()
        context = {
            'proyecto': proyecto, 
            'fluidos': fluidos,
            'materiales':materiales
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        fluido = request.POST.get('fluido')
        material = request.POST.get('material')
        id_proyecto = request.POST.get('id')

        try:
            p = Proyecto.objects.get(pk=id_proyecto)
        except Proyecto.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No existe el proyecto')
            return redirect('proyectos')
        
        if len(nombre) < 2:
            messages.add_message(request, messages.ERROR, 'El nombre del proyecto debe ser mayor a 2 digitos')
            return redirect('proyectos_editar', pk=id_proyecto)

        if fluido == '0':
            messages.add_message(request, messages.ERROR, 'El fluido no es valido')
            return redirect('proyectos_editar', pk=id_proyecto)
        
        if material == '0':
            messages.add_message(request, messages.ERROR, 'El material no es valido')
            return redirect('proyectos_editar', pk=id_proyecto)


        f = Fluido.objects.get(pk=fluido)
        m = Material.objects.get(pk=material)
        p.nombre = nombre
        p.fluido = f
        p.material = m
        p.save()

        messages.add_message(request, messages.SUCCESS, 'Proyecto editado con exito')
        return redirect('proyectos')

class ProyectoDeleteView(generic.DeleteView):
    template_name = "sections/proyectos/delete.html"
    def get(self, request, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=kwargs['pk'])
        context = {
            'proyecto': proyecto
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        Proyecto.objects.filter(pk=kwargs['pk']).delete()
        messages.add_message(request, messages.SUCCESS, 'Proyecto eliminado')
        return redirect('proyectos')


def borrarTuberia(request, pk):
    Tuberia.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def borrarNodo(request, pk):
    Nodo.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
def borrarReservorio(request, pk):
    Reservorio.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def obtenerProyectoDatos(request, pk):

    tuberias = json.loads(serialize("json", Tuberia.objects.filter(proyecto=pk)))
    nodos = json.loads(serialize("json", Nodo.objects.filter(proyecto=pk)))
    reservorios = json.loads(serialize("json", Reservorio.objects.filter(proyecto=pk)))
    
    tarray = []
    for t in tuberias:
        tarray.append(t['fields'])

    narray = []
    for n in nodos:
        narray.append(n['fields'])

    rarray = []
    for r in reservorios:
        rarray.append(r['fields'])

    context = {
        'tuberias' : tarray,
        'nodos' : narray,
        'reservorios' : rarray,
    }

    return JsonResponse(context, safe=False)
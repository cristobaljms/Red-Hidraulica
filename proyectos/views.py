from django.shortcuts import render
from .models import Proyecto, Nodo, Tuberia, Reservorio
from materiales.models import Material
from fluidos.models import Fluido
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
from django.http import JsonResponse
import math
import re
import json
import numpy as np
from numpy import inf

class ProyectoAdminView(generic.CreateView):
    template_name = "sections/proyectos/show.html"

    def get(self, request, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=kwargs['pk'])
        nodos = Nodo.objects.filter(proyecto=proyecto)
        tuberias = Tuberia.objects.filter(proyecto=proyecto).order_by('numero')
        reservorios = Reservorio.objects.filter(proyecto=proyecto)

        sreservorios = json.loads(serialize("json", reservorios))
        snodos = json.loads(serialize("json", nodos))

        rarray = []

        for sr in sreservorios:
            fields = sr['fields']
            fields['pktype'] = 'r'+str(sr['pk'])
            rarray.append(fields)

        for sn in snodos:
            fields = sn['fields']
            fields['pktype'] = 'n'+str(sn['pk'])
            rarray.append(fields)

        context = {
            'proyecto': proyecto,
            'nodos':nodos,
            'tuberias':tuberias,
            'reservorios': reservorios,
            'opciones_tuberia': rarray 
        }
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        tipo = request.POST.get('tipo')
        id_proyecto = request.POST.get('id_proyecto')

        if (tipo == 'nodo'):
            numero = request.POST.get('numero')
            demanda = request.POST.get('demanda')
            cota = request.POST.get('cota')
            x_position = request.POST.get('x_position')
            y_position = request.POST.get('y_position')
            proyecto = Proyecto.objects.get(pk=id_proyecto)
            nodo = Nodo(proyecto=proyecto, numero=numero, cota=cota, demanda=demanda, x_position=x_position, y_position=y_position)
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

            if start == end:
                messages.add_message(request, messages.ERROR, 'El nodo de inicio no puede ser igual al nodo final')
                return redirect('proyecto_administrar', id_proyecto)

            if(re.match('n', start)):
                patron = re.compile('n')
                nstart = Nodo.objects.get(pk = int(patron.split(start)[1]))  
            else:
                patron = re.compile('r')
                nstart = Reservorio.objects.get(pk = int(patron.split(start)[1]))

            if(re.match('n', end)):
                patron = re.compile('n')
                nend = Nodo.objects.get(pk = int(patron.split(end)[1]))  
            else:
                patron = re.compile('r')
                nend = Reservorio.objects.get(pk = int(patron.split(end)[1]))

            proyecto = Proyecto.objects.get(pk=id_proyecto)
            tuberia = Tuberia(proyecto=proyecto, numero=numero, longitud=longitud, diametro=diametro, start=nstart.numero, end = nend.numero)
            tuberia.save()
            messages.add_message(request, messages.SUCCESS, 'Tuberia creada con exito')
            return redirect('proyecto_administrar', id_proyecto)
        else:
            numero = request.POST.get('numero')
            z = request.POST.get('z')
            x_position = request.POST.get('x_position')
            y_position = request.POST.get('y_position')
            
            proyecto = Proyecto.objects.get(pk=id_proyecto)
            reservorio = Reservorio(numero=numero, z=z, proyecto=proyecto, y_position=y_position, x_position=x_position)
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


def getProjectData(pk):
    tuberias = json.loads(serialize("json", Tuberia.objects.filter(proyecto=pk).order_by('numero')))
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
    return context

def obtenerProyectoDatos(request, pk):
    return JsonResponse(getProjectData(pk), safe=False)


def f_calculo(Re, rf_D, fhijo=0.001, error=0.001):
    ban = False
    if(Re<=2200):
        f = 64/Re
    else:
        Xi = 1/math.sqrt(fhijo)
        ban = True
        while(ban):
            fx = -2*np.log10((rf_D/3.7)+((2.51*Xi)/Re))
            dividendo = 2.51/Re
            divisor = ((rf_D/3.7)) + (( 2.51*Xi ) / Re )
            Fx = ( -2/np.log(10) ) * (dividendo/divisor)
            Xi_1 = Xi - (fx-Xi)/(Fx-1)
            compare = abs(Xi_1-Xi)
            if(compare<=error):
                f = 1/pow(Xi,2)
                ban = False
            else:
                Xi = Xi_1
    return f

def printTabla(ntuberias, Qx, Lx, A,V,f,hf,Km,hm,hfhm,a, af):
        V = np.round(V, 4)
        A = np.round(A, 4)
        hf = np.round(hf, 4)
        Km = np.round(Km, 4)
        hm = np.round(hm, 4)
        hfhm = np.round(hfhm, 4)
        a = np.round(a, 4)
        af = np.round(af, 4)
        f = np.round(f,4)
        print("T  | Qx  |  Lx   |    A   |    V   |   f    |    hf  |Km|  hm   |  hfhm   |   a   |     af")
        for i in range(0,ntuberias):
            #print("T"+str(i),'|', af[i])
            print("T"+str(i),'|', Qx[i],'|', Lx[i],'|', A[i],'|', V[i], '|', f[i], '|', hf[i], '|', Km[i],'|', hm[i],'|', hfhm[i], '|', a[i],'|', af[i],)


def infToZeros(arreglo):
    dimension = arreglo.shape
    for i in range(0, dimension[0]):
        for j in range(0, dimension[1]):
            if(arreglo[i,j] == inf):
                arreglo[i,j] = 0
    return arreglo

from numpy.linalg import inv
def H_calculo(A12, A21, A10, A11, H0, q, N, I, Qx, ntuberias, nnodos, nreservorios):
    
    step1 = inv(N*A11)
    print("inv(N*A11)")
    print(step1)
    step2 = A21*step1
    print("A21*inv(N*A11)")
    print(step2)
    step3 = step2*A12
    print("(A21*inv(N*A11))*A12")
    print(step3)
    step4 = inv(step3) * -1
    print("inv(A21*inv(N*A11)*A12)*-1")
    print(step4)

    step5 = Qx.dot(A11) + A10.dot(H0)
    print("[A11][Q]+[A10][H0]")
    print(step5)
    step5 = np.reshape(step5, (ntuberias,1))
    
    #print(step5)
    step6 = step2.dot(step5)
    print("[A21]([N][A11])^-1*([A11][Q]+[A10][H0])")
    print(step6)
    #print(step2)
    Qx = np.reshape(Qx, (ntuberias,1))
    step7 = A21.dot(Qx)
    print("A21*Q")
    print(step7)
    step8 = step7 - q 
    print("(A21*Q)-q")
    print(step8)

    step9 = step6 - step8
    print("[A21]([N][A11])^-1*([A11][Q]+[A10][H0])-([A21][Q]-[q])")
    print(step9)
    
    step10 = step4.dot(step9)
    print("todas las H")
    print(step10)

    Qstep1 = inv(N*A11)
    print("Qstep1 inv(N*A11)")
    print(Qstep1)
    Qstep2 = Qstep1*A11
    print("Qstep2 inv(N*A11)*A11")
    print(Qstep2)
    Qstep3 = I - Qstep2
    print("Qstep3 I - inv(N*A11)*A11")
    print(Qstep3)
    Qx = np.reshape(Qx, (ntuberias,1))
    Qstep4 = Qstep3.dot(Qx)
    print("Qstep4 (I - inv(N*A11)*A11) * Q")
    print(Qstep4)
    Qstep5 = A10 * H0
    print("Qstep5 A10 * H0")
    print(Qstep5)
    Qstep6 = A12 * step10
    print("Qstep6 [A12][Hi+1]")
    print(Qstep6)
    Qstep7 = Qstep6 + Qstep5
    print("Qstep7 [A10][H0]+[A12][Hi+1]")

    print("________________________")
    print(Qstep1)
    print(Qstep7)
    Qstep8 = Qstep1.dot(Qstep7)

    print("Qstep8 (([N][A11])^-1)*([A10][H0]+[A12][Hi+1])")
    print(Qstep8)
    Qstep9 = Qstep4 - Qstep8

    print("todas las Q")
    print(Qstep9)

    # print(A12)
    # print("A21")
    # print(A21)
    # print("A10")
    # print(A10)
    # print("A11")
    # print(A11)
    # print("H0")
    # print(H0)
    # print("q")
    # print(q)
    # print("N")
    # print(N)
    # print("I")
    # print(I)
    # print("Qx")
    # print(Qx)

def Q_calculo(step, Hs, A12, A21, A10, A11, H0, q, N, I, Qx, ntuberias, nnodos, nreservorios):
    Qstep1 = inv(N*A11)
    print("inv(N*A11)")
    print(Qstep1)
    Qstep1 = Qstep1*A11
    print("inv(N*A11)*A11")
    print(Qstep1)
    Qstep1 = I - Qstep1
    print("I - inv(N*A11)*A11")
    print(Qstep1)
    Qx = np.reshape(Qx, (ntuberias,1))
    Qstep1 = Qstep1.dot(Qx)
    print("(I - inv(N*A11)*A11) * Q")
    print(Qstep1)
    Qstep2 = A10 * H0
    print("A10 * H0")
    print(Qstep2)
    Qstep3 = A12 * Hs
    print("[A12][Hi+1]")
    print(Qstep3)
    Qstep4 = Qstep2 + Qstep3
    print("[A10][H0]+[A12][Hi+1]")
    print(Qstep4)

def CalculosGradiente(request, pk):
    data = getProjectData(pk)
    proyecto = Proyecto.objects.get(pk=pk)

    ntuberias = len(data['tuberias'])
    nnodos = len(data['nodos'])
    nreservorios = len(data['reservorios'])

    array_longitud = []
    for t in data['tuberias']:
        array_longitud.append(t['longitud'])
    
    array_diametro = []
    for t in data['tuberias']:
        array_diametro.append(t['diametro'])

    Qx = np.zeros(ntuberias) + 0.1
    Lx = np.array(array_longitud)
    Dx = np.array(array_diametro)
    A = (np.pi*np.power(Dx,2))/4
    V = Qx/A

    Ks   = np.zeros(ntuberias) + 0.00006
    Re   = np.zeros(ntuberias) + V*Dx/proyecto.fluido.valor_viscocidad
    Re = np.round(Re, 0)
    f = []
    for i in range(0,ntuberias):
        f.append(f_calculo(Re[i],Ks[i]/Dx[i]))

    hf   = np.zeros(ntuberias) + f*(Lx/Dx)*(np.power(V,2)/(2*9.81))
    Km   = np.zeros(ntuberias).astype(int) + [0,10,0,0,0,0,0]
    hm   = np.zeros(ntuberias) + Km * (np.power(V,2)/(2*9.81))
    hfhm = np.zeros(ntuberias) + (hf + hm)
    a    = np.zeros(ntuberias) + (hfhm / np.power(Qx, 2))
    af   = np.zeros(ntuberias) + (a * Qx)
    printTabla(ntuberias, Qx, Lx, A,V,f,hf,Km,hm,hfhm,a, af)
    # 1.- Matriz de conectividad
    A12 = []

    for tuberia in data['tuberias']:
        a = np.zeros(nnodos).astype(int)
        for i in range(0, nnodos):
            if(tuberia['start'] == data['nodos'][i]['numero']):
                a[i] = -1
        for i in range(0, nnodos):
            if(tuberia['end'] == data['nodos'][i]['numero']):
                a[i] = 1
        A12.append(a)
    
    A12 = np.matrix(A12)
    
    # Matrix traspuesta de A12
    A21 = A12.transpose()

    # Matrix topologica
    # A10 = np.zeros((ntuberias, nreservorios)).astype(int)
    A10 = []
    for tuberia in data['tuberias']:
        a = np.zeros(nreservorios).astype(int)
        for i in range(0, nreservorios):
            if(tuberia['start'] == data['reservorios'][i]['numero'] or tuberia['end'] == data['reservorios'][i]['numero']):
                a[i] = -1
        A10.append(a)
    A10 = np.matrix(A10)
    
    # Matriz diagonal 
    A11 = np.zeros((ntuberias, ntuberias))
    for i in range(0, len(af)):
        A11[i][i] = af[i]
    
    # Arreglo alturas de reservorios
    H0 = []
    for reservorio in data['reservorios']:
        H0.append(reservorio['z'])
    
    H0 = np.array(H0)

    # Arreglo caudal de salida
    q = []
    for nodo in data['nodos']:
        q.append(nodo['demanda'])
    
    q = np.array(q)
    q = np.reshape(q, (nnodos,1))

    # Matriz diagonal del 2 y matriz identidad
    N = np.zeros((ntuberias, ntuberias)).astype(int)
    I = np.zeros((ntuberias, ntuberias)).astype(int)
    for i in range(0, ntuberias):
        N[i][i] = 2
        I[i][i] = 1
    

    H_calculo(A12, A21, A10, A11, H0, q, N, I, Qx, ntuberias, nnodos, nreservorios)

    #Q_calculo(Hs, A12, A21, A10, A11, H0, q, N, I, Qx, ntuberias, nnodos, nreservorios)
    #printTabla(ntuberias, Qx, Lx, A,V,f,hf,Km,hm,hfhm,a, af)
    return JsonResponse(getProjectData(pk), safe=False)


from django.shortcuts import render
from .models import Proyecto, Nodo, Tuberia, Reservorio
from materiales.models import Material
from fluidos.models import Fluido
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.core.serializers import serialize
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
from io import BytesIO
from numpy import inf
from numpy.linalg import inv
from django.core.files.storage import FileSystemStorage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
import numpy as np
import math
import re
import json

class ProyectoAdminView(generic.CreateView):
    template_name = "sections/proyectos/show.html"

    def get(self, request, *args, **kwargs):
        proyecto = Proyecto.objects.get(pk=kwargs['pk'])
        nodos = Nodo.objects.filter(proyecto=proyecto)
        tuberias = Tuberia.objects.filter(proyecto=proyecto).order_by('orden')
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

        torden = 1
        for t in tuberias:
            torden = t.orden

        context = {
            'proyecto': proyecto,
            'nodos':nodos,
            'tuberias':tuberias,
            'torden': torden + 1,
            'reservorios': reservorios,
            'opciones_tuberia': rarray,
            'active_tab': kwargs['active_tab'], 
        }
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        tipo = request.POST.get('tipo')
        id_proyecto = request.POST.get('id_proyecto')

        if (tipo == 'nodo'):
            active_tab = 'n'
            numero = request.POST.get('numero')
            demanda = request.POST.get('demanda')
            cota = request.POST.get('cota')
            x_position = request.POST.get('x_position')
            y_position = request.POST.get('y_position')
            proyecto = Proyecto.objects.get(pk=id_proyecto)
            nodo = Nodo(proyecto=proyecto, numero=numero, cota=cota, demanda=demanda, x_position=x_position, y_position=y_position)
            nodo.save()
            messages.add_message(request, messages.SUCCESS, 'Nodo creado con exito')
            return redirect('proyecto_administrar', id_proyecto, active_tab)

        elif (tipo == 'tuberia'):
            active_tab = 't'
            numero = request.POST.get('numero')
            longitud = request.POST.get('longitud')
            diametro = request.POST.get('diametro')
            km = request.POST.get('km')
            orden = request.POST.get('orden')
            start = request.POST.get('start')
            end = request.POST.get('end')

            if start == '0' or end == '0':
                messages.add_message(request, messages.ERROR, 'Debe ingresar el nodo incial y el nodo final')
                return redirect('proyecto_administrar', id_proyecto, active_tab)

            if start == end:
                messages.add_message(request, messages.ERROR, 'El nodo de inicio no puede ser igual al nodo final')
                return redirect('proyecto_administrar', id_proyecto, active_tab)

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
            tuberia = Tuberia(proyecto=proyecto, numero=numero, orden=orden, longitud=longitud, diametro=diametro, km=km, start=nstart.numero, end = nend.numero)
            tuberia.save()
            messages.add_message(request, messages.SUCCESS, 'Tuberia creada con exito')
            return redirect('proyecto_administrar', id_proyecto, active_tab)
        else:
            active_tab = 'r'
            numero = request.POST.get('numero')
            z = request.POST.get('z')
            x_position = request.POST.get('x_position')
            y_position = request.POST.get('y_position')
            
            proyecto = Proyecto.objects.get(pk=id_proyecto)
            reservorio = Reservorio(numero=numero, z=z, proyecto=proyecto, y_position=y_position, x_position=x_position)
            reservorio.save()
            messages.add_message(request, messages.SUCCESS, 'Reservorio creado con exito')
            return redirect('proyecto_administrar', id_proyecto, active_tab)

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

class TuberiaUpdateView(generic.View):

    def post(self, request, *args, **kwargs):
        active_tab = 't'
        id_tuberia = kwargs['pk']
        id_proyecto = request.POST.get('id_proyecto')
        numero = request.POST.get('numero')
        longitud = request.POST.get('longitud')
        diametro = request.POST.get('diametro')
        km = request.POST.get('km')
        orden = request.POST.get('orden')
        start = request.POST.get('mstart')
        end = request.POST.get('mend')

        if start == '0' or end == '0':
            messages.add_message(request, messages.ERROR, 'Debe ingresar el nodo incial y el nodo final')
            return redirect('proyecto_administrar', id_proyecto, active_tab)

        if start == end:
            messages.add_message(request, messages.ERROR, 'El nodo de inicio no puede ser igual al nodo final')
            return redirect('proyecto_administrar', id_proyecto, active_tab)

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

        tuberia = Tuberia.objects.get(pk=id_tuberia)
        tuberia.numero=numero
        tuberia.orden=orden
        tuberia.longitud=longitud
        tuberia.diametro=diametro
        tuberia.km=km
        tuberia.start=nstart.numero
        tuberia.end = nend.numero
        tuberia.save()

        messages.add_message(request, messages.SUCCESS, 'Tuberia actualizada con exito')
        return redirect('proyecto_administrar', id_proyecto, active_tab)

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
    tuberias = json.loads(serialize("json", Tuberia.objects.filter(proyecto=pk).order_by('orden')))
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

def TableFormatter(ntuberias,tuberias, Qx, Lx, Dx, A,V,Re, f,hf,Km,hm,hfhm,a, af):
        V = np.round(V, 4)
        A = np.round(A, 4)
        Qx = np.round(Qx, 4)
        hf = np.round(hf, 4)
        Km = np.round(Km, 4)
        hm = np.round(hm, 4)
        hfhm = np.round(hfhm, 4)
        a = np.round(a, 4)
        af = np.round(af, 4)
        f = np.round(f,4)
        tabla = []
        for i in range(0,ntuberias):
            tabla.append({
                'tuberia': "{}-{}".format(tuberias[i]['start'],tuberias[i]['end']),
                'Qx':Qx[i], 
                'Lx': Lx[i], 
                'Dx': Dx[i],
                'A': A[i], 
                'V': V[i],
                'Re': Re[i],  
                'f': f[i], 
                'hf': hf[i], 
                'Km': Km[i], 
                'hm': hm[i], 
                'hfhm': hfhm[i], 
                'a': a[i],   
                'af': af[i]
            })
        return tabla

def infToZeros(arreglo):
    dimension = arreglo.shape
    for i in range(0, dimension[0]):
        for j in range(0, dimension[1]):
            if(arreglo[i,j] == inf):
                arreglo[i,j] = 0
    return arreglo

def validateError(Error):
    flag = False
    dimension = Error.shape
    for i in range(0, dimension[0]):
        for j in range(0, dimension[1]):
            if(Error[i,j] > 0.001):
                flag = True
    return flag

def calculosGradiente(iteracion, pk, Qx, H, response):
    data = getProjectData(pk)
    proyecto = Proyecto.objects.get(pk=pk)
    iteracionRow = { "iteracion": iteracion }

    ntuberias = len(data['tuberias'])
    nnodos = len(data['nodos'])
    nreservorios = len(data['reservorios'])
    
    array_longitud = []
    for t in data['tuberias']:
        array_longitud.append(t['longitud'])
    
    array_diametro = []
    for t in data['tuberias']:
        array_diametro.append(t['diametro'])
    
    array_km = []
    for t in data['tuberias']:
        array_km.append(t['km'])

    aux_qx = Qx
    for i in range(0,ntuberias):
        if (Qx[i] < 0):
            Qx[i] = Qx[i] * -1

    Lx = np.array(array_longitud)
    Dx = np.array(array_diametro)
    A = (np.pi*np.power(Dx,2))/4
    V = Qx/A
    Ks   = np.zeros(ntuberias) + proyecto.material.ks
    Re   = np.zeros(ntuberias) + V*Dx/proyecto.fluido.valor_viscocidad
    Re = np.round(Re, 0)
    f = []
    for i in range(0,ntuberias):
        f.append(f_calculo(Re[i],Ks[i]/Dx[i]))

    hf   = np.zeros(ntuberias) + f*(Lx/Dx)*(np.power(V,2)/(2*9.81))
    Km = np.array(array_km)

    hm   = np.zeros(ntuberias) + Km * (np.power(V,2)/(2*9.81))
    hfhm = np.zeros(ntuberias) + (hf + hm)
    a    = np.zeros(ntuberias) + (hfhm / np.power(Qx, 2))
    af   = np.zeros(ntuberias) + (a * Qx)

    table = TableFormatter(ntuberias,data['tuberias'], Qx, Lx, Dx, A,V,Re, f,hf,Km,hm,hfhm,a, af)
    iteracionRow['tabla'] = table
    
    # 1.- Matriz de conectividad
    A12 = []

    i = 0
    for tuberia in data['tuberias']:
        a = np.zeros(nnodos).astype(int)
        for i in range(0, nnodos):
            if(tuberia['start'] == data['nodos'][i]['numero']):
                a[i] = -1
        for i in range(0, nnodos):
            if(tuberia['end'] == data['nodos'][i]['numero']):
                a[i] = 1
        if (aux_qx[i] < 0):
            a = a * -1
        A12.append(a)
    
    A12 = np.matrix(A12)
    print("\n\n------------------Iteracion {}--------------------".format(iteracion))
    print("Matriz A12")
    print(A12)
    # Matrix traspuesta de A12
    A21 = A12.transpose()
    print("\nMatriz A21 Matriz traspuesta de A12")
    print(A21)
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
    print("\nMatriz topologica A10")
    print(A10)
    # Matriz diagonal 
    A11 = np.zeros((ntuberias, ntuberias))
    for i in range(0, len(af)):
        A11[i][i] = af[i]
    
    print("\nMatriz diagonal A11")
    print(np.round(A11,4))
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
    print("\nArreglo caudal de salida q")
    print(q)
    # Matriz diagonal del 2 y matriz identidad
    N = np.zeros((ntuberias, ntuberias)).astype(int)
    I = np.zeros((ntuberias, ntuberias)).astype(int)
    for i in range(0, ntuberias):
        N[i][i] = 2
        I[i][i] = 1
    
    print("\nMatriz diagonal del 2 y matriz identidad")
    print(N)
    print(I)
    # Calculamos las H
    step1 = inv(N*A11)
    print("\n([N][A11])^-1")
    print(np.round(step1,4))

    step2 = A21*step1
    print("\n[A21]([N][A11])^-1")
    print(np.round(step2,4))

    step3 = step2*A12
    print("\n([A21]([N][A11])^-1)*([A12]")
    print(np.round(step3,4))

    step4 = inv(step3) * -1
    print("\n-(([A21]([N][A11])^-1)*([A12])^-1")
    print(np.round(step4,4))

    Qx = np.reshape(Qx, ntuberias)
    step5 = Qx.dot(A11) + A10.dot(H0)
    step5 = np.reshape(step5, (ntuberias,1))
    print("\n[A11][Q]+[A10][H0]")
    print(np.round(step5,4))

    step6 = step2.dot(step5)
    print("\n[A21]([N][A11])^-1*([A11][Q]+[A10][H0])")
    print(np.round(step6,4))

    Qx = np.reshape(Qx, (ntuberias,1))
    step7 = A21.dot(Qx)
    step8 = step7 - q 
    step9 = step6 - step8
    step10 = step4.dot(step9)
    
    iteracionRow['H'] = np.squeeze(np.asarray(np.round(step10,4))).tolist()
    print("\ntodas las H")
    print(np.round(step10,4))

    # Calculamos las Q
    Qstep1 = inv(N*A11)
    Qstep2 = Qstep1*A11
    Qstep3 = I - Qstep2
    Qx = np.reshape(Qx, (ntuberias,1))
    Qstep4 = Qstep3.dot(Qx)
    Qstep5 = A10 * H0
    Qstep6 = A12 * step10
    Qstep7 = Qstep6 + Qstep5
    Qstep8 = Qstep1.dot(Qstep7)
    Qstep9 = Qstep4 - Qstep8
    
    iteracionRow['Qx'] = np.squeeze(np.asarray(np.round(Qstep9, 4))).tolist()
    #print("todas las Q")
    #print(Qstep9)
    
    iteracion = iteracion + 1
    if(len(H) > 0):
        error = np.absolute(H-step10)
        iteracionRow['error'] = np.squeeze(np.asarray(np.round(error,4))).tolist()
        response.append(iteracionRow)
        if (validateError(error)):
            Qstep9 = np.squeeze(np.asarray(Qstep9))
            return calculosGradiente(iteracion, pk, Qstep9, step10, response)
        else:
            return response
    else:
        response.append(iteracionRow)
        Qstep9 = np.squeeze(np.asarray(Qstep9))
        return calculosGradiente(iteracion, pk, Qstep9, step10, response)

class GradienteView(generic.View):
    template_name = "sections/calculos/gradiente.html"

    def get(self, request, *args, **kwargs):
        data = getProjectData(kwargs['pk'])
        ntuberias = len(data['tuberias'])
        qx = 0
        for nodo in data['nodos']:
            qx = qx + nodo['demanda']
        Qx = np.zeros(ntuberias) + (qx/ntuberias)
        context = {
            'data': calculosGradiente(1, kwargs['pk'], Qx, [], []),
            'project_pk': kwargs['pk']
        }
        #return JsonResponse(context, safe=False)
        return render(request, self.template_name, context)

def GradienteToPDFView(request, pk):
    data = getProjectData(pk)
    ntuberias = len(data['tuberias'])
    
    qx = 0
    for nodo in data['nodos']:
        qx = qx + nodo['demanda']
    Qx = np.zeros(ntuberias) + (qx/ntuberias)

    calculos = calculosGradiente(1, pk, Qx, [], [])

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4))
    Story = []

    ps_head = ParagraphStyle('titulo',alignment = TA_CENTER, fontSize = 14, fontName="Times-Roman")
    ps_iteracion = ParagraphStyle('titulo',alignment = TA_JUSTIFY, fontSize = 12, fontName="Times-Roman")
    ps_tabla = ParagraphStyle('titulo',alignment = TA_JUSTIFY, fontSize = 8, fontName="Times-Roman")

    text = "<b>METODO DE LA GRADIENTE</b>"
    p = Paragraph(text, ps_head)
    Story.append(p)
    Story.append(Spacer(1,0.5*inch))

    titles = [
        Paragraph('<b>Tuberia</b>', ps_tabla),
        Paragraph('<b>Caudal</b>', ps_tabla),
        Paragraph('<b>Longitud</b>', ps_tabla),
        Paragraph('<b>Diametro</b>', ps_tabla),
        Paragraph('<b>Area</b>', ps_tabla),
        Paragraph('<b>Velocidad</b>', ps_tabla),
        Paragraph('<b>Re</b>', ps_tabla),
        Paragraph('<b>f</b>', ps_tabla),
        Paragraph('<b>hf+hm</b>', ps_tabla),
        Paragraph('<b>a</b>', ps_tabla),
        Paragraph('<b>af</b>', ps_tabla)
    ]
    
    for iteracion in calculos:
        text = "<b>Iteracion {}</b>".format(iteracion['iteracion'])
        p = Paragraph(text, ps_iteracion)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))

        table_formatted = [titles]
        for i in iteracion['tabla']:
            tuberia = i['tuberia']
            Qx = i['Qx']
            Lx = i['Lx']
            Dx = i['Dx']
            A = i['A']
            V = i['V']
            Re = i['Re']
            f = i['f']
            hfhm = i['hfhm']
            a = i['a']
            af = i['af']
            row = [ tuberia, Qx, Lx, Dx, A, V,Re, f, hfhm, a, af ]
            table_formatted.append(row)


        t=Table(table_formatted, (60,40,60,60,60,60,50,40,100,100,100))
        for each in range(len(iteracion['tabla'])):
            if each % 2 == 0:
                bg_color = colors.white
            else:
                bg_color = '#c9c9c9'
            t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(9,0),'#878787'),
            ('INNERGRID',(0,0),(9,0), 0.25, colors.gray),
            ('BOX',(0,0),(9,0), 0.25, colors.gray)
        ]))

        Story.append(t)
        Story.append(Spacer(1,0.2*inch))

        THtitles = [ 
            Paragraph('H', ps_tabla)
        ]
        table_formatted = [THtitles]
        for value in iteracion['H']:
            table_formatted.append([value])

        t=Table(table_formatted, (40))
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(1,0),colors.lightgrey),
            ('INNERGRID',(0,0),(1,0), 0.25, colors.gray),
            ('BOX',(0,0),(1,0), 0.25, colors.gray)
        ]))
        Story.append(t)
        Story.append(Spacer(1,0.2*inch))

        TQxtitles = [ 
            Paragraph('Qx', ps_tabla)
        ]

        table_formatted = [TQxtitles]
        for value in iteracion['Qx']:
            table_formatted.append([value])

        t=Table(table_formatted, (40))
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(1,0),colors.lightgrey),
            ('INNERGRID',(0,0),(1,0), 0.25, colors.gray),
            ('BOX',(0,0),(1,0), 0.25, colors.gray)
        ]))
        Story.append(t)
        Story.append(Spacer(1,0.2*inch))


        TErrortitles = [ 
            Paragraph('Error', ps_tabla)
        ]

        table_formatted = [TErrortitles]

        if 'error' in iteracion:
            for value in iteracion['error']:
                table_formatted.append([value])

            t=Table(table_formatted, (40))
            t.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(1,0),colors.lightgrey),
                ('INNERGRID',(0,0),(1,0), 0.25, colors.gray),
                ('BOX',(0,0),(1,0), 0.25, colors.gray)
            ]))
            Story.append(t)
            Story.append(Spacer(1,0.2*inch))

        table_formatted = [titles]
        Story.append(Spacer(1,0.2*inch))

    proyecto = Proyecto.objects.get(pk=pk)

    doc.build(Story)
    pdf_value = pdf_buffer.getvalue()
    pdf_buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="gradientmethod.pdf"'
    response.write(pdf_value)
    return response

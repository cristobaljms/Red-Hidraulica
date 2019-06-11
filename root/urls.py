from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import  login
from proyectos.views import GeneticoToPDFView, GeneticView, borrarDiametroGenetico, DiametroGeneticoUpdateView, NodoUpdateView, TuberiaUpdateView,GradienteToExcelView, GradienteToPDFView, GradienteView, obtenerProyectoDatos, ProyectosListView, ProyectosCreateView, ProyectosUpdateView, ProyectoDeleteView, ProyectoAdminView, borrarTuberia, borrarNodo, borrarReservorio
from materiales.views import MaterialesListView, MaterialesCreateView, MaterialesUpdateView, MaterialesDeleteView
from fluidos.views import FluidosListView, FluidosCreateView, FluidosUpdateView, FluidosDeleteView
from django.contrib.auth.decorators import login_required
from proyectos.utils import poll_state

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(ProyectosListView.as_view(), login_url='/login/'), name='proyectos'),
    path('proyectos/crear/', login_required(ProyectosCreateView.as_view(), login_url='/login/'), name='proyectos_crear'),
    path('proyectos/editar/<int:pk>/', login_required(ProyectosUpdateView.as_view(), login_url='/login/'), name='proyectos_editar'),
    path('proyectos/eliminar/<int:pk>/', login_required(ProyectoDeleteView.as_view(), login_url='/login/'), name='proyecto_eliminar'),
    path('proyectos/administrar/<int:pk>/<slug:active_tab>', login_required(ProyectoAdminView.as_view(), login_url='/login/'), name='proyecto_administrar'),
    path('proyecto/datos/<int:pk>/', login_required(obtenerProyectoDatos, login_url='/login/'), name='get_project_data'),
    path('tuberia/eliminar/<int:pk>/', login_required(borrarTuberia, login_url='/login/'), name='tuberia_eliminar'),
    path('tuberia/actualizar/<int:pk>/', login_required(TuberiaUpdateView.as_view(), login_url='/login/'), name='tuberia_editar'),
    path('reservorio/eliminar/<int:pk>/', login_required(borrarReservorio, login_url='/login/'), name='nodo_eliminar'),
    path('nodo/eliminar/<int:pk>/', login_required(borrarNodo, login_url='/login/'), name='nodo_eliminar'),
    path('nodo/actualizar/<int:pk>/', login_required(NodoUpdateView.as_view(), login_url='/login/'), name='nodo_editar'),
    path('genetico/eliminar/<int:pk>/', login_required(borrarDiametroGenetico, login_url='/login/'), name='genetico_eliminar'),
    path('genetico/actualizar/<int:pk>/', login_required(DiametroGeneticoUpdateView.as_view(), login_url='/login/'), name='genetico_editar'),
    path('calculos/gradiente/<int:pk>/', login_required(GradienteView.as_view(), login_url='/login/'), name='calculo_gradiente'),
    path('calculos/genetico/<int:pk>/', login_required(GeneticView.as_view(), login_url='/login/'), name='calculo_genetico'),
    path('calculos/genetico/<int:pk>/<int:bin>', login_required(GradienteView.as_view(), login_url='/login/'), name='calculo_gradiente'),
    path('reporte/pdf/gradiente/<int:pk>/', login_required(GradienteToPDFView, login_url='/login/'), name='reporte_pdf_gradiente'),
    path('reporte/pdf/genetico/<int:pk>/', login_required(GeneticoToPDFView, login_url='/login/'), name='reporte_pdf_genetico'),
    path('reporte/excel/gradiente/<int:pk>/', login_required(GradienteToExcelView, login_url='/login/'), name='reporte_excel_gradiente'),
    path('materiales/', login_required(MaterialesListView.as_view(), login_url='/login/'), name='materiales'),
    path('materiales/crear/', login_required(MaterialesCreateView.as_view(), login_url='/login/'), name='materiales_crear'),
    path('materiales/editar/<int:pk>/', login_required(MaterialesUpdateView.as_view(), login_url='/login/'), name='materiales_editar'),
    path('materiales/eliminar/<int:pk>/', login_required(MaterialesDeleteView.as_view(), login_url='/login/'), name='materiales_eliminar'),
    path('fluidos/', login_required(FluidosListView.as_view(), login_url='/login/'), name='fluidos'),
    path('fluidos/crear/', login_required(FluidosCreateView.as_view(), login_url='/login/'), name='fluidos_crear'),
    path('fluidos/editar/<int:pk>/', login_required(FluidosUpdateView.as_view(), login_url='/login/'), name='fluidos_editar'),
    path('fluidos/eliminar/<int:pk>/', login_required(FluidosDeleteView.as_view(), login_url='/login/'), name='fluidos_eliminar'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('poll_state/', poll_state, name='poll_state')
]
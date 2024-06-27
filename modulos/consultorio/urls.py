from django.urls import path # type: ignore
from . import views
from django.contrib.auth.views import * # type: ignore

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('pacientes/', views.listar_pacientes, name='pacientes'),
    path('paciente/crear/', views.crear_paciente, name='crear_paciente'),
    path('paciente/<int:pk>/modificar/', views.modificar_paciente, name='editar_paciente'),
    path('paciente/<int:pk>/eliminar/', views.eliminar_paciente, name='eliminar_paciente'),
    path('medicos/', views.listar_medicos, name='medicos'),
    path('medicos/agregar/', views.agregar_medico, name='agregar_medico'),
    path('medicos/editar/<int:pk>/', views.editar_medico, name='editar_medico'),
    path('medicos/eliminar/<int:pk>/', views.eliminar_medico, name='eliminar_medico'),
    path('paciente/<int:paciente_id>/ficha_medica/', views.ficha_medica, name='ficha_medica_paciente'),
    path('generar_consulta/<int:paciente_id>/', views.generar_consulta_paciente, name='generar_consulta_paciente'),
    path('reportes/', views.generar_consulta_paciente, name='reportes'),
    path('reportes1/', views.reporte_consultas, name='reportes1'),
]
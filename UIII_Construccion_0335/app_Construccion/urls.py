from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_construccion, name='inicio_construccion'),
    path('empleado/agregar/', views.agregar_empleado, name='agregar_empleado'),
    path('empleado/ver/', views.ver_empleados, name='ver_empleados'),
    path('empleado/actualizar/<int:empleado_id>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('empleado/realizar_actualizacion/<int:empleado_id>/', views.realizar_actualizacion_empleado, name='realizar_actualizacion_empleado'),
    path('empleado/borrar/<int:empleado_id>/', views.borrar_empleado, name='borrar_empleado'),
]
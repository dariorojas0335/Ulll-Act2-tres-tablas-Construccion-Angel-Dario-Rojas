from django.contrib import admin
from .models import Empleado, Cliente, Proyecto

admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Proyecto)
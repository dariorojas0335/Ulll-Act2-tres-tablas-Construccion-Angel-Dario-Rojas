# Proyecto Django: Sistema de Administración de Construcción

Te proporcionaré una guía completa para crear el proyecto de construcción con Django, incluyendo todos los archivos necesarios.

## 1. Estructura inicial del proyecto

Primero, vamos a crear la estructura completa de carpetas y archivos:

```
UIII_Construccion_0335/
├── backend_Construccion/
│   ├── backend_Construccion/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── app_Construccion/
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── templates/
│   │   │   ├── app_Construccion/
│   │   │   │   ├── empleado/
│   │   │   │   │   ├── agregar_empleado.html
│   │   │   │   │   ├── ver_empleado.html
│   │   │   │   │   ├── actualizar_empleado.html
│   │   │   │   │   └── borrar_empleado.html
│   │   │   │   ├── base.html
│   │   │   │   ├── header.html
│   │   │   │   ├── navbar.html
│   │   │   │   ├── footer.html
│   │   │   │   └── inicio.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── db.sqlite3
└── .venv/
```

## 2. Procedimientos paso a paso

### Pasos 1-3: Crear carpeta y abrir VS Code
```bash
# Crear carpeta del proyecto
mkdir UIII_Construccion_0335
cd UIII_Construccion_0335

# Abrir VS Code en esta carpeta
code .
```

### Pasos 4-6: Entorno virtual
En la terminal de VS Code:
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Mac/Linux:
source .venv/bin/activate

# Verificar que está activado (debería mostrar (.venv) al inicio)
```

### Pasos 7-8: Instalar Django y crear proyecto
```bash
# Instalar Django
pip install django

# Crear proyecto (sin duplicar carpeta)
django-admin startproject backend_Construccion .
```

### Paso 9-10: Ejecutar servidor
```bash
# Ejecutar en puerto 8032
python manage.py runserver 8032
```

### Paso 11: Crear aplicación
```bash
python manage.py startapp app_Construccion
```

## 3. Archivos del proyecto

### 3.1 models.py (corregido)
```python
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_cliente = models.CharField(
        max_length=50,
        choices=[
            ("Residencial", "Residencial"),
            ("Comercial", "Comercial"),
            ("Gubernamental", "Gubernamental"),
        ],
        default="Residencial"
    )
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"

class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="proyectos")
    empleados = models.ManyToManyField(Empleado, related_name="proyectos")
    estado = models.CharField(
        max_length=50,
        choices=[
            ("En planificación", "En planificación"),
            ("En curso", "En curso"),
            ("Finalizado", "Finalizado"),
        ],
        default="En planificación",
    )

    def __str__(self):
        return self.nombre
```

### 3.2 views.py
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado

def inicio_construccion(request):
    return render(request, 'app_Construccion/inicio.html')

def agregar_empleado(request):
    if request.method == 'POST':
        empleado = Empleado(
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            cargo=request.POST['cargo'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            fecha_contratacion=request.POST['fecha_contratacion'],
            salario=request.POST['salario']
        )
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'app_Construccion/empleado/agregar_empleado.html')

def ver_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'app_Construccion/empleado/ver_empleado.html', {'empleados': empleados})

def actualizar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.cargo = request.POST['cargo']
        empleado.telefono = request.POST['telefono']
        empleado.email = request.POST['email']
        empleado.fecha_contratacion = request.POST['fecha_contratacion']
        empleado.salario = request.POST['salario']
        empleado.save()
        return redirect('ver_empleados')
    return render(request, 'app_Construccion/empleado/actualizar_empleado.html', {'empleado': empleado})

def realizar_actualizacion_empleado(request, empleado_id):
    return actualizar_empleado(request, empleado_id)

def borrar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('ver_empleados')
    return render(request, 'app_Construccion/empleado/borrar_empleado.html', {'empleado': empleado})
```

### 3.3 urls.py (app_Construccion)
```python
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
```

### 3.4 urls.py (backend_Construccion)
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_Construccion.urls')),
]
```

### 3.5 settings.py (agregar app)
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_Construccion',  # Agregar esta línea
]
```

### 3.6 admin.py
```python
from django.contrib import admin
from .models import Empleado, Cliente, Proyecto

admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Proyecto)
```

## 4. Templates

### 4.1 base.html
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Administración Construcción</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .navbar-brand {
            font-weight: bold;
            color: #2c3e50 !important;
        }
        .bg-primary {
            background-color: #3498db !important;
        }
        .btn-primary {
            background-color: #3498db;
            border-color: #3498db;
        }
        .btn-primary:hover {
            background-color: #2980b9;
            border-color: #2980b9;
        }
        .card {
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .footer {
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            margin-top: 50px;
        }
    </style>
</head>
<body>
    {% include 'app_Construccion/header.html' %}
    {% include 'app_Construccion/navbar.html' %}
    
    <div class="container mt-4">
        {% block content %}
        {% endblock %}
    </div>
    
    {% include 'app_Construccion/footer.html' %}

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 4.2 navbar.html
```html
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
        <a class="navbar-brand" href="{% url 'inicio_construccion' %}">
            🏗️ Sistema de Administración Construcción
        </a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'inicio_construccion' %}">
                        🏠 Inicio
                    </a>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👥 Empleados
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="{% url 'agregar_empleado' %}">Agregar Empleado</a></li>
                        <li><a class="dropdown-item" href="{% url 'ver_empleados' %}">Ver Empleados</a></li>
                    </ul>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        📋 Proyectos
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Agregar Proyecto</a></li>
                        <li><a class="dropdown-item" href="#">Ver Proyectos</a></li>
                    </ul>
                </li>
                
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                        👨‍💼 Clientes
                    </a>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="#">Agregar Cliente</a></li>
                        <li><a class="dropdown-item" href="#">Ver Clientes</a></li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### 4.3 inicio.html
```html
{% extends 'app_Construccion/base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title text-primary">Bienvenido al Sistema de Administración de Construcción</h2>
                <p class="card-text">
                    Este sistema permite gestionar de manera eficiente todos los aspectos de su empresa de construcción:
                </p>
                <ul>
                    <li>Gestión de empleados y recursos humanos</li>
                    <li>Control de proyectos de construcción</li>
                    <li>Administración de clientes</li>
                    <li>Seguimiento de presupuestos y tiempos</li>
                </ul>
                <p class="card-text">
                    Utilice el menú de navegación para acceder a las diferentes secciones del sistema.
                </p>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body text-center">
                <img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=500&q=80" 
                     alt="Construcción" class="img-fluid rounded">
                <p class="mt-3 text-muted">Sistema desarrollado para optimizar procesos constructivos</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 4.4 footer.html
```html
<footer class="footer mt-5">
    <div class="container text-center">
        <p>&copy; {% now "Y" %} Sistema de Administración Construcción - Todos los derechos reservados</p>
        <p>Fecha del sistema: {% now "d/m/Y H:i" %}</p>
        <p><strong>Creado por Tec. Angel Dario Rojas, Cbtis 128</strong></p>
    </div>
</footer>
```

### 4.5 agregar_empleado.html
```html
{% extends 'app_Construccion/base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">Agregar Nuevo Empleado</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" name="nombre" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="apellido" class="form-label">Apellido</label>
                            <input type="text" class="form-control" id="apellido" name="apellido" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="cargo" class="form-label">Cargo</label>
                        <input type="text" class="form-control" id="cargo" name="cargo" required>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="telefono" class="form-label">Teléfono</label>
                            <input type="text" class="form-control" id="telefono" name="telefono" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="fecha_contratacion" class="form-label">Fecha de Contratación</label>
                            <input type="date" class="form-control" id="fecha_contratacion" name="fecha_contratacion" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="salario" class="form-label">Salario</label>
                            <input type="number" step="0.01" class="form-control" id="salario" name="salario" required>
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'ver_empleados' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-primary">Guardar Empleado</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 4.6 ver_empleado.html
```html
{% extends 'app_Construccion/base.html' %}

{% block content %}
<div class="card">
    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h4 class="mb-0">Lista de Empleados</h4>
        <a href="{% url 'agregar_empleado' %}" class="btn btn-light">➕ Agregar Empleado</a>
    </div>
    <div class="card-body">
        {% if empleados %}
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Nombre</th>
                        <th>Apellido</th>
                        <th>Cargo</th>
                        <th>Teléfono</th>
                        <th>Email</th>
                        <th>Salario</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {% for empleado in empleados %}
                    <tr>
                        <td>{{ empleado.nombre }}</td>
                        <td>{{ empleado.apellido }}</td>
                        <td>{{ empleado.cargo }}</td>
                        <td>{{ empleado.telefono }}</td>
                        <td>{{ empleado.email }}</td>
                        <td>${{ empleado.salario }}</td>
                        <td>
                            <div class="btn-group" role="group">
                                <a href="{% url 'actualizar_empleado' empleado.id %}" class="btn btn-warning btn-sm">✏️ Editar</a>
                                <a href="{% url 'borrar_empleado' empleado.id %}" class="btn btn-danger btn-sm">🗑️ Borrar</a>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% else %}
        <div class="alert alert-info text-center">
            <h5>No hay empleados registrados</h5>
            <p>Comienza agregando el primer empleado al sistema.</p>
            <a href="{% url 'agregar_empleado' %}" class="btn btn-primary">Agregar Primer Empleado</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### 4.7 actualizar_empleado.html
```html
{% extends 'app_Construccion/base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-warning text-dark">
                <h4 class="mb-0">Actualizar Empleado</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    {% csrf_token %}
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" name="nombre" value="{{ empleado.nombre }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="apellido" class="form-label">Apellido</label>
                            <input type="text" class="form-control" id="apellido" name="apellido" value="{{ empleado.apellido }}" required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label for="cargo" class="form-label">Cargo</label>
                        <input type="text" class="form-control" id="cargo" name="cargo" value="{{ empleado.cargo }}" required>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="telefono" class="form-label">Teléfono</label>
                            <input type="text" class="form-control" id="telefono" name="telefono" value="{{ empleado.telefono }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" name="email" value="{{ empleado.email }}" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <label for="fecha_contratacion" class="form-label">Fecha de Contratación</label>
                            <input type="date" class="form-control" id="fecha_contratacion" name="fecha_contratacion" value="{{ empleado.fecha_contratacion|date:'Y-m-d' }}" required>
                        </div>
                        <div class="col-md-6 mb-3">
                            <label for="salario" class="form-label">Salario</label>
                            <input type="number" step="0.01" class="form-control" id="salario" name="salario" value="{{ empleado.salario }}" required>
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <a href="{% url 'ver_empleados' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-warning">Actualizar Empleado</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 4.8 borrar_empleado.html
```html
{% extends 'app_Construccion/base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h4 class="mb-0">Confirmar Eliminación</h4>
            </div>
            <div class="card-body text-center">
                <h5>¿Está seguro que desea eliminar al empleado?</h5>
                <p class="lead">{{ empleado.nombre }} {{ empleado.apellido }}</p>
                <p><strong>Cargo:</strong> {{ empleado.cargo }}</p>
                <p><strong>Email:</strong> {{ empleado.email }}</p>
                
                <form method="POST">
                    {% csrf_token %}
                    <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <a href="{% url 'ver_empleados' %}" class="btn btn-secondary me-md-2">Cancelar</a>
                        <button type="submit" class="btn btn-danger">Confirmar Eliminación</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 5. Comandos finales para ejecutar

### Paso 12.5: Realizar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Paso 27: Registrar modelos y migraciones
```bash
# Ya están registrados en admin.py, solo hacer migraciones
python manage.py makemigrations
python manage.py migrate
```

### Paso 31: Ejecutar servidor
```bash
python manage.py runserver 8032
```

## 6. Comprobación final

1. Navegar a `http://localhost:8032` para ver la página de inicio
2. Probar la funcionalidad CRUD completa de empleados
3. Verificar que todos los templates se muestren correctamente
4. Confirmar que el sistema es totalmente funcional

El proyecto está listo con colores suaves y modernos, interfaz atractiva y todas las funcionalidades solicitadas para la gestión de empleados.

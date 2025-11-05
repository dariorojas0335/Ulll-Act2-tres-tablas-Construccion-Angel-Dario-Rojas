Perfecto 👍
Aquí tienes **la versión lista para copiar y pegar directamente en un documento de GitHub (README.md, PDF, Word, etc.)** — con formato limpio en Markdown, bloques de código bien delimitados, y pasos numerados exactamente como los pediste.

Puedes copiar **todo este bloque completo**:

---

# 🏗️ Proyecto Django — Construcción

**Lenguaje:** Python
**Framework:** Django
**Editor:** VS Code

---

## 📁 Primera Parte — Procedimiento paso a paso

### 1️⃣ Crear carpeta del Proyecto `UIII_Construccion_0335`

```bash
mkdir UIII_Construccion_0335
cd UIII_Construccion_0335
```

### 2️⃣ Abrir VS Code sobre la carpeta

```bash
code .
```

(O también desde VS Code: `File > Open Folder...` y seleccionas la carpeta.)

### 3️⃣ Abrir terminal en VS Code

* Menú: `Terminal > New Terminal`
* Atajo: `Ctrl + ``

### 4️⃣ Crear carpeta de entorno virtual `.venv` desde la terminal

```bash
# Windows PowerShell
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

### 5️⃣ Activar el entorno virtual

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows cmd
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

### 6️⃣ Activar intérprete de Python en VS Code

* En VS Code: `Ctrl + Shift + P` → “Python: Select Interpreter” → elige `.venv`.

### 7️⃣ Instalar Django

```bash
pip install --upgrade pip
pip install django
```

### 8️⃣ Crear proyecto `backend_Construccion` sin duplicar carpeta

```bash
django-admin startproject backend_Construccion
```

### 9️⃣ Ejecutar servidor en el puerto 8032

```bash
cd backend_Construccion
python manage.py runserver 8032
```

### 🔟 Copiar y pegar el link en el navegador

```
http://127.0.0.1:8032/
```

### 11️⃣ Crear aplicación `app_Construccion`

```bash
python manage.py startapp app_Construccion
```

---

## 🧱 12. Archivo `models.py`

Ruta: `backend_Construccion/app_Construccion/models.py`

```python
from django.db import models

# ==========================================
# MODELO: Cliente (PENDIENTE)
# ==========================================
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
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================================
# MODELO: Empleado (ACTIVO)
# ==========================================
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cargo}"


# ==========================================
# MODELO: Proyecto (PENDIENTE)
# ==========================================
class Proyecto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="proyectos", blank=True, null=True)
    empleados = models.ManyToManyField(Empleado, related_name="proyectos", blank=True)
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

---

## 🧩 12.5 Realizar migraciones

```bash
python manage.py makemigrations app_Construccion
python manage.py migrate
```

---

## 👷 13–14. MODELO: Empleado — `views.py`

Ruta: `backend_Construccion/app_Construccion/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Empleado
from django.utils import timezone

def inicio_construccion(request):
    contexto = {"titulo": "Sistema de Administración Construccion", "now_year": timezone.now().year}
    return render(request, "inicio.html", contexto)

def agregar_empleado(request):
    if request.method == "POST":
        Empleado.objects.create(
            nombre=request.POST.get("nombre"),
            apellido=request.POST.get("apellido"),
            cargo=request.POST.get("cargo"),
            telefono=request.POST.get("telefono"),
            email=request.POST.get("email"),
            fecha_contratacion=request.POST.get("fecha_contratacion"),
            salario=request.POST.get("salario"),
        )
        return redirect("ver_empleado")
    return render(request, "empleado/agregar_empleado.html")

def ver_empleado(request):
    empleados = Empleado.objects.all().order_by("-id")
    return render(request, "empleado/ver_empleado.html", {"empleados": empleados, "now_year": timezone.now().year})

def actualizar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    return render(request, "empleado/actualizar_empleado.html", {"empleado": empleado})

def realizar_actualizacion_empleado(request, empleado_id):
    if request.method == "POST":
        empleado = get_object_or_404(Empleado, id=empleado_id)
        empleado.nombre = request.POST.get("nombre")
        empleado.apellido = request.POST.get("apellido")
        empleado.cargo = request.POST.get("cargo")
        empleado.telefono = request.POST.get("telefono")
        empleado.email = request.POST.get("email")
        empleado.fecha_contratacion = request.POST.get("fecha_contratacion")
        empleado.salario = request.POST.get("salario")
        empleado.save()
        return redirect("ver_empleado")
    return HttpResponse("Método no permitido", status=405)

def borrar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == "POST":
        empleado.delete()
        return redirect("ver_empleado")
    return render(request, "empleado/borrar_empleado.html", {"empleado": empleado})
```

---

## 🧭 15–22. Estructura de carpetas y plantillas HTML

```
app_Construccion/
 └─ templates/
     ├─ base.html
     ├─ header.html
     ├─ navbar.html
     ├─ footer.html
     ├─ inicio.html
     └─ empleado/
         ├─ agregar_empleado.html
         ├─ ver_empleado.html
         ├─ actualizar_empleado.html
         └─ borrar_empleado.html
```

---

### 🧱 base.html

```html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}Sistema de Administración Construccion{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background-color: #f7f9fb; color: #333; }
    .card { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.05); }
    footer { background: #ffffff; border-top: 1px solid #eaeaea; padding: 12px 0; }
  </style>
</head>
<body>
  {% include "header.html" %}
  {% include "navbar.html" %}
  <main class="container my-4">
    {% block content %}{% endblock %}
  </main>
  {% include "footer.html" %}
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

---

### 🧭 navbar.html

```html
<nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
  <div class="container">
    <a class="navbar-brand d-flex align-items-center" href="{% url 'inicio_construccion' %}">
      <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" class="bi bi-building" viewBox="0 0 16 16"><path d="M8.5 2.5v5h1v-5h-1z"/><path d="M1 2a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v12h-1V2H1v12H0V2a1 1 0 0 1 1-1z"/></svg>
      <span class="ms-2">Sistema de Administración Construccion</span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="{% url 'inicio_construccion' %}">Inicio</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Empleados</a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="{% url 'agregar_empleado' %}">Agregar empleado</a></li>
            <li><a class="dropdown-item" href="{% url 'ver_empleado' %}">Ver empleados</a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Proyectos</a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Agregar proyectos</a></li>
            <li><a class="dropdown-item" href="#">Ver proyectos</a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">Clientes</a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Agregar clientes</a></li>
            <li><a class="dropdown-item" href="#">Ver clientes</a></li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

---

### 🧾 footer.html

```html
<footer class="fixed-bottom text-center">
  <div class="container">
    <small>
      &copy; {{ now_year }} - Derechos reservados. Creado por Tec. Angel Dario Rojas, Cbtis 128.
    </small>
  </div>
</footer>
```

---

### 🏠 inicio.html

```html
{% extends "base.html" %}
{% block title %}Inicio - Sistema Construccion{% endblock %}
{% block content %}
<div class="row">
  <div class="col-md-7">
    <div class="card p-4">
      <h3>Bienvenido al Sistema de Administración de Construcción</h3>
      <p>Este sistema permite gestionar empleados, proyectos y clientes.</p>
      <ul>
        <li>Agregar, ver, actualizar y borrar empleados.</li>
        <li>Diseño simple, moderno y funcional.</li>
      </ul>
    </div>
  </div>
  <div class="col-md-5">
    <img src="https://images.unsplash.com/photo-1526403224743-7b7f3c5fb7f8?auto=format&fit=crop&w=1200&q=60" class="img-fluid rounded" alt="Construcción">
  </div>
</div>
{% endblock %}
```

---

### 👷 Plantillas de Empleado (`/empleado/`)

#### agregar_empleado.html

```html
{% extends "base.html" %}
{% block content %}
<div class="card p-4">
  <h4>Agregar empleado</h4>
  <form method="post" action="{% url 'agregar_empleado' %}">
    {% csrf_token %}
    <input name="nombre" class="form-control mb-2" placeholder="Nombre">
    <input name="apellido" class="form-control mb-2" placeholder="Apellido">
    <input name="cargo" class="form-control mb-2" placeholder="Cargo">
    <input name="telefono" class="form-control mb-2" placeholder="Teléfono">
    <input name="email" type="email" class="form-control mb-2" placeholder="Correo">
    <input name="fecha_contratacion" type="date" class="form-control mb-2">
    <input name="salario" type="number" step="0.01" class="form-control mb-3" placeholder="Salario">
    <button class="btn btn-primary">Guardar</button>
  </form>
</div>
{% endblock %}
```

#### ver_empleado.html

```html
{% extends "base.html" %}
{% block content %}
<div class="card p-4">
  <h4>Lista de empleados</h4>
  <a href="{% url 'agregar_empleado' %}" class="btn btn-success mb-3">Agregar empleado</a>
  <table class="table table-striped">
    <thead><tr><th>#</th><th>Nombre</th><th>Cargo</th><th>Email</th><th>Acciones</th></tr></thead>
    <tbody>
      {% for e in empleados %}
      <tr>
        <td>{{ forloop.counter }}</td>
        <td>{{ e.nombre }} {{ e.apellido }}</td>
        <td>{{ e.cargo }}</td>
        <td>{{ e.email }}</td>
        <td>
          <a href="{% url 'actualizar_empleado' e.id %}" class="btn btn-sm btn-info">Editar</a>
          <a href="{% url 'borrar_empleado' e.id %}" class="btn btn-sm btn-danger">Borrar</a>
        </td>
      </tr>
      {% empty %}
      <tr><td colspan="5">No hay empleados</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}
```

#### actualizar_empleado.html

```html
{% extends "base.html" %}
{% block content %}
<div class="card p-4">
  <h4>Actualizar empleado</h4>
  <form method="post" action="{% url 'realizar_actualizacion_empleado' empleado.id %}">
    {% csrf_token %}
    <input name="nombre" class="form-control mb-2" value="{{ empleado.nombre }}">
    <input name="apellido" class="form-control mb-2" value="{{ empleado.apellido }}">
    <input name="cargo" class="form-control mb-2" value="{{ empleado.cargo }}">
    <input name="telefono" class="form-control mb-2" value="{{ empleado.telefono }}">
    <input name="email" class="form-control mb-2" value="{{ empleado.email }}">
    <input name="fecha_contratacion" type="date" class="form-control mb-2" value="{{ empleado.fecha_contratacion }}">
    <input name="salario" type="number" step="0.01" class="form-control mb-3" value="{{ empleado.salario }}">
    <button class="btn btn-primary">Actualizar</button>
  </form>
</div>
{% endblock %}
```

#### borrar_empleado.html

```html
{% extends "base.html" %}
{% block content %}
<div class="card p-4">
  <h4>Eliminar empleado</h4>
  <p>¿Seguro que deseas eliminar a <strong>{{ empleado.nombre }} {{ empleado.apellido }}</strong>?</p>
  <form method="post">
    {% csrf_token %}
    <button class="btn btn-danger">Sí, eliminar</button>
    <a href="{% url 'ver_empleado' %}" class="btn btn-secondary">Cancelar</a>
  </form>
</div>
{% endblock %}
```

---

## 🌐 24. Archivo `urls.py` de `app_Construccion`

Ruta: `app_Construccion/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio_construccion, name="inicio_construccion"),
    path("empleados/", views.ver_empleado, name="ver_empleado"),
    path("empleados/agregar/", views.agregar_empleado, name="agregar_empleado"),
    path("empleados/actualizar/<int:empleado_id>/", views.actualizar_empleado, name="actualizar_empleado"),
    path("empleados/realizar_actualizacion/<int:empleado_id>/", views.realizar_actualizacion_empleado, name="realizar_actualizacion_empleado"),
    path("empleados/borrar/<int:empleado_id>/", views.borrar_empleado, name="borrar_empleado"),
]
```

---

## ⚙️ 25. Agregar `app_Construccion` en `settings.py`

En `backend_Construccion/settings.py`:

```python
INSTALLED_APPS = [
    # apps de Django
    'app_Construccion',
]
```

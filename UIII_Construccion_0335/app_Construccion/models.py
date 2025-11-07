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

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Habitacion(models.Model):
    idHab         = models.AutoField(primary_key=True)
    nombre        = models.CharField(max_length=50)
    servicio      = models.ForeignKey('servicio', on_delete=models.CASCADE)
    dispHab       = models.ForeignKey('dispHab', on_delete=models.CASCADE)
    descripcion   = models.CharField(max_length=550)
    imagen        = models.ImageField(upload_to='habitaciones/imagenes')
    ytVidId       = models.CharField(max_length=11, null=True)
    precio        = models.IntegerField()
    capacidad     = models.IntegerField()
    tipoHab       = models.ForeignKey('tipoHab', on_delete=models.CASCADE)

class tipoHab(models.Model):
    idTipo        = models.IntegerField(primary_key=True)
    nombre        = models.CharField(max_length=20)

class imgHab(models.Model):
    idImg         = models.AutoField(primary_key=True)
    idHab         = models.ForeignKey('Habitacion', on_delete=models.CASCADE)
    imagen        = models.ImageField(upload_to='habitaciones/capturas')

class servicio(models.Model):
    idServ         = models.AutoField(primary_key=True)
    nombre        = models.CharField(max_length=50)

class dispHab(models.Model):
    idDisp        = models.AutoField(primary_key=True)
    nombre        = models.CharField(max_length=40)

class Serie(models.Model):
    idSerie       = models.IntegerField(primary_key=True)
    estudio       = models.CharField(max_length=50, null=True)
    nombre        = models.CharField(max_length=50)
    descripcion   = models.CharField(max_length=220)
    fechalanz     = models.DateField(default='2000-01-01')
    precio        = models.IntegerField()
    imagen        = models.ImageField(upload_to='series/imagenes')
    stock         = models.IntegerField()
    clave         = models.FileField(upload_to='series/claves_zip/',null= False)
    categoria     = models.ForeignKey('categoriaSerie', on_delete=models.CASCADE)    
    ytVidId       = models.CharField(max_length=11, null=True)

class imagenSerie (models.Model):
    idSerie       = models.ForeignKey('Serie', on_delete=models.CASCADE)    
    idImagen      = models.IntegerField(primary_key=True)
    imagen        = models.ImageField(upload_to='series/imagenes/',null= False)

class categoriaSerie (models.Model):
    idDisp = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)

class Usuario ( models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombre    = models.CharField(max_length=35)
    apellido  = models.CharField(max_length=35)
    rut       = models.CharField(max_length=40, default='11111111-1')
    email     = models.EmailField(max_length=70)
    telefono  = models.CharField(max_length=40)
    region    = models.ForeignKey('Region', on_delete=models.CASCADE)   
    nivelEd   = models.ForeignKey('nivelEducacional', on_delete=models.CASCADE)   
    fechaNac  = models.DateField(default='2000-01-01')

class Region (models.Model):
    idRegion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)

class nivelEducacional(models.Model):
    idEducacion = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=60)

class Carrito(models.Model):
    idCarro = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    reserva = models.ManyToManyField('Habitacion', related_name='carritos', blank=True)
    series = models.ManyToManyField('Serie', related_name='carritos', blank=True)
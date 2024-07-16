from django.contrib import admin
from .models import Habitacion, imgHab, tipoHab, nivelEducacional, Usuario, Region, dispHab, servicio, Reserva

# Register your models here.
admin.site.register(Habitacion)
admin.site.register(Reserva)
admin.site.register(Usuario)
admin.site.register(Region)
admin.site.register(imgHab)
admin.site.register(tipoHab)
admin.site.register(nivelEducacional)
admin.site.register(servicio)
admin.site.register(dispHab)
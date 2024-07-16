from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.principal, name='principal'),
    path('principal', views.verHabitacionesPrincipal, name='verJuegosPrincipal'),
    path('principal', views.principal, name='principal'),
    path('carrito/ver', views.verCarro, name='verCarro'),
    path('registroUsuarios', views.registroUsuarios, name='registroUsuarios'),
    path('registroHab', views.registroHab, name='registroHab'),
    path('registroSeries', views.registroSeries, name='registroSeries'),
    path('<int:idHab>/', views.verHab, name='verHab'),
    path('plantilla', views.plantilla, name='plantilla'),
    path('carrito/agregar/<int:idHab>', views.agregarHabCarro, name='agregarHabCarro'),
    path('carrito/eliminar/<int:idHab>', views.eliminarHabCarro, name='eliminarHabCarro'),    
    path('listadoHabs', views.listadoHabs, name='listadoHabs'),
    path('eliminarHab/<int:idHab>', views.eliminarHab, name='eliminarHab'),
    path('registroHab/<int:idHab>', views.modificarHab, name='modificarHab'),
    path('subirHab', views.subirHab, name='subirHab'),
    path('listadoSeries', views.listadoSeries, name='listadoSeries'),
    path('eliminarSerie/<int:idSerie>', views.eliminarSerie, name='eliminarSerie'),
    path('registroSeries/<int:idSerie>', views.modificarSerie, name='modificarSerie'),
    path('subirSerie', views.subirSerie, name='subirSerie'),
    path('listadoUsuarios', views.listadoUsuarios, name='listadoUsuarios'),
    path('eliminarUsuario/<int:idUsuario>', views.eliminarUsuario, name='eliminarUsuario'),
    path('registroUsuarios/<int:idUsuario>', views.modificarUsuario, name='modificarUsuario'),
    path('registrarse', views.registrarse, name='registrarse'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page='principal'), name='logout'),
    #transbank:
    path('resultado_compra/', views.commit_transaction, name='commit_transaction'),
    path('resultado_compra/', views.resultadoCompra, name='resultadoCompra')
]
from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.principal, name='principal'),
    path('principal', views.verJuegosPrincipal, name='verJuegosPrincipal'),
    path('principal', views.principal, name='principal'),
    path('carrito/ver', views.verCarro, name='verCarro'),
    path('juego', views.juego, name='juego'),
    path('registroUsuarios', views.registroUsuarios, name='registroUsuarios'),
    path('registroJuegos', views.registroJuegos, name='registroJuegos'),
    path('registroSeries', views.registroSeries, name='registroSeries'),
    path('<int:idJuego>/', views.verJuego, name='verJuego'),
    path('plantilla', views.plantilla, name='plantilla'),
    path('carrito/agregar/<int:idJuego>', views.agregarJuegoCarro, name='agregarJuegoCarro'),
    path('carrito/eliminar/<int:idJuego>', views.eliminarJuegoCarro, name='eliminarJuegoCarro'),    
    path('listadoJuegos', views.listadoJuegos, name='listadoJuegos'),
    path('eliminarJuego/<int:idJuego>', views.eliminarJuego, name='eliminarJuego'),
    path('registroJuegos/<int:idJuego>', views.modificarJuego, name='modificarJuego'),
    path('subirJuego', views.subirJuego, name='subirJuego'),
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
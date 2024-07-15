from django.shortcuts import render, redirect
from .models import Juego, Carrito, tipoClave, Serie, imagenSerie,categoriaSerie, imgJuegos, Usuario, Region, nivelEducacional, desarrollador, categoriaJuego
from M2A.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import juegoForm
from .forms import customLoginForm
from django.contrib.auth.views import LoginView,LogoutView
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

#transbank
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
import random


def principal(request):
    return render(request, 'principal.html', {})

def carrito(request):
    carritoSesion = request.session.get('carrito', {})
    return render(request, 'carrito.html', carritoSesion)
# Create your views here.

def juego(request):
    return render(request, 'juegoplantilla copy.html', {})

def registroUsuarios(request):
    regiones = Region.objects.all()
    nivelesEducacionales = nivelEducacional.objects.all()
    context = {
    'regiones': regiones,
    'nivelesEducacionales': nivelesEducacionales,
    }
    return render(request, 'registroUsuarios.html', context)

@login_required
def registroJuegos(request):
    tipoClaves = tipoClave.objects.all()
    desarrolladores = desarrollador.objects.all()
    categorias = categoriaJuego.objects.all()
    context = {
    'tipoClaves': tipoClaves,
    'desarrolladores': desarrolladores,
    'categorias': categorias
    }
    return render(request, 'registroJuegos.html', context)

@login_required
def registroSeries(request):
    categorias = categoriaSerie.objects.all()

    context = {
    'categorias': categorias
    }
    return render(request, 'registroSeries.html', context)

def verJuego(request, idJuego):
    juego = Juego.objects.get(idJuego = idJuego)
    capturas = imgJuegos.objects.filter(idJuego=juego)
    return render(request, 'juegoplantilla.html', {'juego': juego, 'capturas': capturas})

def verJuegosPrincipal(request):
    juegos = Juego.objects.all()
    context = {
    'juegos': juegos,
    'MEDIA_URL': MEDIA_URL 
    }
    return render(request, 'principal.html', context)

def plantilla(request):
    return render(request, 'plantilla_base.html', {})


def agregarJuegoCarro(request, idJuego):
    context = {}
    try:
        usuario = request.user
        item = Juego.objects.get(idJuego = idJuego)
        carritoSesion = request.session.get('carrito', {})
        if str(idJuego) in carritoSesion:
            carritoSesion[str(idJuego)]['cantidad'] += 1
        else:
            carritoSesion[str(idJuego)] = {
            'idJuego': str(item.idJuego),
            'nombre' : item.nombre,
            'precio' : str(item.precio),
            'stock'  : item.stock,
            'imagen' : item.imagen.url if item.imagen else '',
            'cantidad': 1
                }
        request.session['carrito'] = carritoSesion

        return redirect(verCarro)
    except:
        context['error'] = 'Error al agregar el producto'
        return render(request, 'carrito.html', context)


def verCarro(request):
    context = {}
    carritoSesion = request.session.get('carrito', {})
    request.session['carrito'] = carritoSesion
    context['listado'] = carritoSesion

    total = 0
    for item in carritoSesion.values():
        total = total + int(item['precio']) * int(item['cantidad'])
    total_coniva = round(total * 1.19)
    
    if total == 0 and request.method == 'POST':
            context['error'] = 'El carro está vacío';
    elif  total > 0:
        print("entré al request post")
        monto = total_coniva
        print("-------------", monto, "-------------")
        ordenCompra = str(random.randint(10000000, 9999999999))
        id_sesion = str(request.session._session_key)
        return_url = "http://127.0.0.1:8000/resultado_compra"
        tx = Transaction(WebpayOptions(Transaction.COMMERCE_CODE, Transaction.API_KEY_SECRET, IntegrationType.TEST))
        response = tx.create(buy_order=ordenCompra, session_id=id_sesion, amount=monto, return_url=return_url)
        print(response)
        context['response'] = response
        request.session['token_ws'] = response['token']
    
    return render(request, 'carrito.html', context)
        #'url': response['url'],
       # 'token': response['token']
   #})

#transbank

def commit_transaction(request):
    context = {}
    try:
        token = request.session.get('token_ws')
        if not token:
            context['error'] = 'Token no encontrado. Si ya realizó la compra intente volver al menú.'
        else:
            tx = Transaction(WebpayOptions(Transaction.COMMERCE_CODE, Transaction.API_KEY_SECRET, IntegrationType.TEST))
            response = tx.commit(token)
            status = response.get('status', 'ERROR')

            if status == 'AUTHORIZED':
                context['response'] = response
                context['success_message'] = 'Pago realizado exitosamente.'
            elif status == 'REVERSED':
                context['error'] = 'El pago fue cancelado.'
            else:
                context['error'] = 'Error en la transacción. Por favor, intente de nuevo.'

            del request.session['carrito']
            del request.session['token_ws']
    except Exception as e:
        context['error'] = 'Compra cancelada'

    return render(request, 'resultado_compra.html', context)

    
def resultadoCompra(request):
    return render(request, 'resultado_compra.html')


def eliminarJuegoCarro(request, idJuego):
    context = {}
    try:
        carritoSesion = request.session.get('carrito', {})
        if str(idJuego) in carritoSesion:
            if carritoSesion[str(idJuego)]['cantidad'] > 1:
                print("Cantidad superior a uno (llego aquí)")
                carritoSesion[str(idJuego)]['cantidad'] -= 1
                print("Intento eliminarlo")
            else:
                # si solo hay uno se elimina.
                del carritoSesion[str(idJuego)]
        request.session['carrito'] = carritoSesion
        return redirect(verCarro)
        #usuario = request.user
        #listado = Carrito.objects.get(usuario = usuario)
        #juego = listado.juegos.get(idJuego = idJuego)
        #listado = listado.juegos
        #listado.remove(juego)
        #context['exito'] = 'Producto eliminado del carrito'
    except:
        context['error'] = 'Error al eliminar el producto'
        return redirect(verCarro)

# juegos:
@login_required
def listadoJuegos(request):
    juegos = Juego.objects.all()
    tipoClaves = tipoClave.objects.all()
    context = {
    'juegos': juegos,
    'tipoClaves': tipoClaves 
    }
    return render(request, 'listadoJuegos.html', context)

@login_required
def eliminarJuego(request, idJuego):
    context = {}
    try:
        juego = Juego.objects.get(idJuego = idJuego)
        juego.delete()
        context['exito'] = 'Juego eliminado con éxito'
    except:
        context['error'] = 'Error al eliminar el juego'
    
    juegos = Juego.objects.all()
    context['juegos'] = juegos
    return render(request, 'listadoJuegos.html', context)

@login_required
def subirJuego(request):
    context = {'form': juegoForm()}
    if request.method == 'POST':
        idJuego       = request.POST['txtId']
        nombre        = request.POST['nombre']
        descripcion   = request.POST['descripcion']
        ytVidId       = request.POST['link']
        precio        = request.POST['precio']
        stock         = request.POST['stock']

        # buscar youtube id
        #m =  re.search(r"([\d\w-_]{11})", ytVidId)
        #ytVidId = m.group()
        
        #convertir idjuego en un string para comparar
        str(idJuego)
        if 'enviarJuego' in request.POST:
            if idJuego == "0":
                 juego1= Juego.objects.create(
                    nombre = nombre,
                    desarrollador = desarrollador.objects.get(idDev=request.POST['desarrollador']),
                    categoria = categoriaJuego.objects.get(idCategoria=request.POST['categoriaJuego']),
                    descripcion = descripcion,
                    imagen = request.FILES['imagen'],
                    ytVidId = ytVidId,
                    precio = precio,
                    stock = stock,
                    clave = request.FILES['archivo'],
                    tipoClave = tipoClave.objects.get(idTipo=request.POST['tipoClave'])
                    )
                 if request.FILES.getlist('captura'):
                    capturas = request.FILES.getlist('captura')
                    for imagen in capturas:
                        imgJuegos.objects.create(
                            idJuego = juego1,
                            imagen = imagen
                        )
            else:
                juego = Juego.objects.get(idJuego = request.POST['txtId'])
                juego.nombre = nombre
                juego.desarrollador = desarrollador.objects.get(idDev=request.POST['desarrollador'])
                juego.categoria = categoriaJuego.objects.get(idCategoria=request.POST['categoriaJuego'])
                juego.descripcion = descripcion
                juego.ytVidId = ytVidId
                juego.precio = precio
                juego.stock = stock
                juego.tipoClave = tipoClave.objects.get(idTipo=request.POST['tipoClave'])
                if 'imagen' in request.FILES:
                    juego.imagen = request.FILES['imagen']
                if 'archivo' in request.FILES:
                    juego.clave = request.FILES['archivo']
                juego.save()
                if request.FILES.getlist('captura'):
                    capturas = request.FILES.getlist('captura')
                    capturas_old = imgJuegos.objects.filter(idJuego=juego)
                    for old in capturas_old:
                        old.delete()
                    for imagen in capturas:
                        imgJuegos.objects.create(
                            idJuego = juego,
                            imagen = imagen
                        )
                
    #context['juegos'] = Juego.objects.all()
    #return render(request, 'listadoJuegos.html', context)
    return redirect(listadoJuegos)

@login_required
def modificarJuego(request, idJuego):
    juego = Juego.objects.get(idJuego = idJuego)
    tipoClaves = tipoClave.objects.all()
    capturas = imgJuegos.objects.filter(idJuego=juego)
    desarrolladores = desarrollador.objects.all()
    categorias = categoriaJuego.objects.all()
    urlCapturas = ""
    for i in capturas:
        urlCapturas += i.imagen.url + " "
    context = {
    'juego': juego,
    'tipoClaves': tipoClaves,
    'desarrolladores': desarrolladores,
    'categorias': categorias,
    'capturas' : capturas,
    'urlCapturas' : urlCapturas
    }
    return render(request, 'registroJuegos.html', context)


#series:

@login_required
def listadoSeries(request):
    series = Serie.objects.all()
    categorias = categoriaSerie.objects.all()
    context = {
    'series': series,
    'categorias': categorias 
    }
    return render(request, 'listadoSeries.html', context)

@login_required
def eliminarSerie(request, idSerie):
    context = {}
    try:
        serie = Serie.objects.get(idSerie = idSerie)
        serie.delete()
        context['exito'] = 'Serie eliminada con éxito'
    except:
        context['error'] = 'Error al eliminar la Serie'
    
    serie = Serie.objects.all()
    context['serie'] = serie
    return render(request, 'listadoSeries.html', context)

@login_required
def subirSerie(request):
    context = {}
    if request.method == 'POST':
        
        idSerie         = request.POST['txtId']
        nombre          = request.POST['titulo']
        estudio         = request.POST['estudio']
        descripcion     = request.POST['descripcion']
        precio          = request.POST['precio']
        stock           = request.POST['stock']
        ytVidId         = request.POST['link']
        fechalanz       = request.POST['lanzamiento']
        
        # buscar youtube id
        ##m =  re.search(r"([\d\w-_]{11})", ytVidId)
        #ytVidId = m.group()
        
        #convertir idserie en un string para comparar
        str(idSerie)
        if 'enviarSerie' in request.POST:
            if idSerie == "0":
                 Serie.objects.create(
                    nombre = nombre,
                    estudio = estudio,
                    descripcion = descripcion,
                    imagen = request.FILES['imagen'],
                    ytVidId = ytVidId,
                    precio = precio,
                    stock = stock,
                    clave = request.FILES['archivo'],
                    fechalanz = fechalanz,
                    categoria = categoriaSerie.objects.get(idCategoria=request.POST['categoria'])
                    )
                 context['exito'] = "Serie creada con éxito"
            else:
                serie = Serie.objects.get(idSerie = request.POST['txtId'])
                serie.nombre = nombre
                serie.estudio = estudio
                serie.descripcion = descripcion
                serie.ytVidId = ytVidId
                serie.precio = precio
                serie.stock = stock
                serie.fechalanz = fechalanz
                serie.categoria = categoriaSerie.objects.get(idCategoria=request.POST['categoria'])
                if 'imagen' in request.FILES:
                    serie.imagen = request.FILES['imagen']
                if 'archivo' in request.FILES:
                    serie.clave = request.FILES['archivo']
                serie.save()
                context['exito'] = "Serie actualizada con éxito"
                
    context['series'] = Serie.objects.all()
    return render(request, 'listadoSeries.html', context)

@login_required
def modificarSerie(request, idSerie):
    serie = Serie.objects.get(idSerie = idSerie)
    categorias = categoriaSerie.objects.all()
    context = {
    'serie': serie,
    'categorias': categorias,
    }
    return render(request, 'registroSeries.html', context)

#usuarios:
@login_required
def listadoUsuarios(request):
    usuario = Usuario.objects.all()
    regiones = Region.objects.all()
    nivelesEducacionales = nivelEducacional.objects.all()
    context = {
    'usuario': usuario,
    'regiones': regiones,
    'nivelesEducacionales': nivelesEducacionales,
    }
    return render(request, 'listadoUsuarios.html', context)

@login_required
def eliminarUsuario(request, idUsuario):
    context = {}
    try:
        usuario = Usuario.objects.get(idUsuario = idUsuario)
        userDjango = User.objects.get(id = idUsuario)
        usuario.delete()
        userDjango.delete()
        context['exito'] = 'Usuario eliminado con éxito'
    except:
        context['error'] = 'Error al eliminar el Usuario'
    
    usuarios = Usuario.objects.all()
    context['usuario'] = usuarios
    return render(request, 'listadoUsuarios.html', context)


def registrarse(request):
    context = {}
    if request.method == 'POST':
        idUsuario = request.POST['txtId']
        nombre    = request.POST['txtNombre']
        apellido  = request.POST['txtApellido']
        rut       = request.POST['txtRut']
        email     = request.POST['txtEmail']
        telefono  = request.POST['txtTelefono']
        fechaNac  = request.POST['edad']
        #convertir idusuario en un string para comparar
        str(idUsuario)
        if 'enviarRegistro' in request.POST:
            print("pasó a enviar registro")
            if idUsuario == "0":
                print("pasó a idusuario")
                try:
                    usuario_existente = Usuario.objects.get(rut=rut)
                    context['error'] = "El rut ya existe"
                    messages.error(request, "El rut ya existe")
                    return redirect('registroUsuarios')
                    #return render(request, 'registroUsuarios.html', context)
                except ObjectDoesNotExist:
                    pass
                Usuario.objects.create(
                    nombre = nombre,
                    apellido = apellido,
                    rut = rut,
                    email = email,
                    telefono = telefono,
                    region = Region.objects.get(idRegion=request.POST['txtRegion']),
                    nivelEd = nivelEducacional.objects.get(idEducacion=request.POST['txtNvlEducacional']),
                    fechaNac = fechaNac
                    )
                userCreado = Usuario.objects.get(rut = rut)
                user = User.objects.create_user(
                    id = userCreado.idUsuario,
                    username = email,
                    email = email,
                    password = (rut[0:4])
                )
                user.set_password(rut[0:4])
                user.save()

                auth_user = authenticate(request, username=email, password=rut[0:4])
                if auth_user is not None:
                    print("hizo el request user")
                    login(request, auth_user)
                    return redirect('principal')
            
            else:
                usuario = Usuario.objects.get(idUsuario = request.POST['txtId'])
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.rut = rut
                usuario.email = email
                usuario.telefono = telefono
                usuario.fechaNac = fechaNac
                usuario.region = Region.objects.get(idRegion=request.POST['txtRegion'])
                usuario.nivelEd = nivelEducacional.objects.get(idEducacion=request.POST['txtNvlEducacional'])
                usuario.save()
            
                print("pasó al otro else")
                user = User.objects.get(id = usuario.idUsuario)
                user.username = email
                user.email = email
                user.set_password(rut[0:4]) 
                user.save()
                messages.success(request, "Usuario modificado con éxito")
                return redirect('listadoUsuarios')  
    context['usuario'] = Usuario.objects.all()
    return render(request, 'registroUsuarios.html', context)


def modificarUsuario(request, idUsuario):
    usuario = Usuario.objects.get(idUsuario = idUsuario)
    nivelesEducacionales = nivelEducacional.objects.all()
    regiones = Region.objects.all()
    context = {
    'usuario': usuario,
    'nivelesEducacionales': nivelesEducacionales,
    'regiones': regiones,
    }
    return render(request, 'registroUsuarios.html', context)


class CustomLoginView(LoginView):
    template_name = 'login.html' 
    authentication_form = customLoginForm
    redirect_authenticated_user = True





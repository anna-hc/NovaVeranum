from django.shortcuts import render, redirect
from .models import Habitacion, Carrito, tipoHab, imgHab, Usuario, Region, nivelEducacional, servicio, dispHab, Reserva
from M2A.settings import MEDIA_URL
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import habForm
from .forms import customLoginForm
from django.contrib.auth.views import LoginView,LogoutView
import datetime
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

def registroUsuarios(request):
    regiones = Region.objects.all()
    nivelesEducacionales = nivelEducacional.objects.all()
    context = {
    'regiones': regiones,
    'nivelesEducacionales': nivelesEducacionales,
    }
    return render(request, 'registroUsuarios.html', context)

@login_required
def registroHab(request):
    tipoHabs = tipoHab.objects.all()
    servicios = servicio.objects.all()
    disponibilidad = dispHab.objects.all()
    context = {
    'tipoHabs': tipoHabs,
    'servicios': servicios,
    'disponibilidad': disponibilidad
    }
    return render(request, 'registroHab.html', context)

@login_required
def registroReservas(request):
    reservas = Reserva.objects.all()
    habitaciones = Habitacion.objects.all()
    context = {
    'reservas': reservas,
    'habitaciones': habitaciones
    }
    return render(request, 'registroReservas.html', context)

def verHab(request, idHab):
    habitacion = Habitacion.objects.get(idHab = idHab)
    capturas = imgHab.objects.filter(idHab = habitacion)
    return render(request, 'habiplantilla.html', {'habitacion': habitacion, 'capturas': capturas})

def verHabitacionesPrincipal(request):
    habitaciones = Habitacion.objects.all()
    context = {
    'habitaciones': habitaciones,
    'MEDIA_URL': MEDIA_URL 
    }
    return render(request, 'principal.html', context)

def plantilla(request):
    return render(request, 'plantilla_base.html', {})


def agregarHabCarro(request, idHab):
    error = 0
    context = {}
    if request.method == 'POST':
        fecha = request.POST['fechaReserva']
        dias = request.POST['cantidadDias']
        try:
            reservas = Reserva.objects.filter(habitacion=idHab)
            inicio = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
            fin = inicio + datetime.timedelta(days=int(dias))
            for reserva in reservas:
                fecha1 = datetime.datetime.strptime(str(reserva.fecha), "%Y-%m-%d")
                for i in range(int(reserva.dias)):
                    # print(fecha1)
                    if inicio<= fecha1 <= fin:
                        inicio1=datetime.datetime.strptime(str(reserva.fecha), "%Y-%m-%d")
                        fin1 = inicio1 + datetime.timedelta(days=int(reserva.dias)-1)
                        messages.error(request, f"La habitación estará reservada durante esa fecha ({inicio1.strftime("%d/%m/%Y")} - {fin1.strftime("%d/%m/%Y")})")
                        return redirect('verHab', idHab=idHab)
                    fecha1=fecha1 + datetime.timedelta(days=1)
                else:
                    usuario = request.user
                    item = Habitacion.objects.get(idHab = idHab)
                    carritoSesion = request.session.get('carrito', {})
                    carritoSesion[str(idHab)] = {
                    'idHab': str(item.idHab),
                    'nombre' : item.nombre,
                    'precio' : str(item.precio),
                    'capacidad'  : item.capacidad,
                    'imagen' : item.imagen.url if item.imagen else '',
                    'cantidad': dias,
                    'fecha' : fecha
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


def eliminarHabCarro(request, idHab):
    context = {}
    try:
        carritoSesion = request.session.get('carrito', {})
        if str(idHab) in carritoSesion:
            del carritoSesion[str(idHab)]
        request.session['carrito'] = carritoSesion
        return redirect(verCarro)
        #usuario = request.user
        #listado = Carrito.objects.get(usuario = usuario)
        #habitacion = listado.habitaciones.get(idHab = idHab)
        #listado = listado.habitaciones
        #listado.remove(habitacion)
        #context['exito'] = 'Producto eliminado del carrito'
    except:
        context['error'] = 'Error al eliminar la reserva'
        return redirect(verCarro)

# habitaciones:
@login_required
def listadoHabs(request):
    habitaciones = Habitacion.objects.all()
    tipoHabs = tipoHab.objects.all()
    context = {
    'habitaciones': habitaciones,
    'tipoHabs': tipoHabs 
    }
    return render(request, 'listadoHabs.html', context)

@login_required
def eliminarHab(request, idHab):
    context = {}
    try:
        habitacion = Habitacion.objects.get(idHab = idHab)
        habitacion.delete()
        context['exito'] = 'Habitación eliminada con éxito'
    except:
        context['error'] = 'Error al eliminar la habitacion'
    
    habitaciones = Habitacion.objects.all()
    context['habitaciones'] = habitaciones
    return render(request, 'listadoHabs.html', context)

@login_required
def subirHab(request):
    context = {'form': habForm()}
    if request.method == 'POST':
        idHab       = request.POST['txtId']
        nombre        = request.POST['nombre']
        descripcion   = request.POST['descripcion']
        ytVidId       = 0
        precio        = request.POST['precio']
        capacidad         = request.POST['capacidad']

        # buscar youtube id
        #m =  re.search(r"([\d\w-_]{11})", ytVidId)
        #ytVidId = m.group()
        str(idHab)
        if 'enviarHab' in request.POST:
            if idHab == "0":
                 hab = Habitacion.objects.create(
                    nombre = nombre,
                    servicio = servicio.objects.get(idServ=request.POST['servicio']),
                    dispHab = dispHab.objects.get(idDisp=request.POST['dispHab']),
                    descripcion = descripcion,
                    imagen = request.FILES['imagen'],
                    ytVidId = None,
                    precio = precio,
                    capacidad = capacidad,
                    tipoHab = tipoHab.objects.get(idTipo=request.POST['tipoHab'])
                    )
                 if request.FILES.getlist('captura'):
                    capturas = request.FILES.getlist('captura')
                    for imagen in capturas:
                        imgHab.objects.create(
                            idHab = hab ,
                            imagen = imagen
                        )
            else:
                habitacion = Habitacion.objects.get(idHab = request.POST['txtId'])
                habitacion.nombre = nombre
                habitacion.servicio = servicio.objects.get(idServ=request.POST['servicio'])
                habitacion.dispHab = dispHab.objects.get(idDisp=request.POST['dispHab'])
                habitacion.descripcion = descripcion
                habitacion.ytVidId = ytVidId
                habitacion.precio = precio
                habitacion.capacidad = capacidad
                habitacion.tipoHab = tipoHab.objects.get(idTipo=request.POST['tipoHab'])
                if 'imagen' in request.FILES:
                    habitacion.imagen = request.FILES['imagen']
                habitacion.save()
                if request.FILES.getlist('captura'):
                    capturas = request.FILES.getlist('captura')
                    capturas_old = imgHab.objects.filter(idHab=habitacion)
                    for old in capturas_old:
                        old.delete()
                    for imagen in capturas:
                        imgHab.objects.create(
                            idHab = habitacion,
                            imagen = imagen
                        )
                
    #context['habitaciones'] = Habitación.objects.all()
    #return render(request, 'listadoHabs.html', context)
    return redirect(listadoHabs)

@login_required
def modificarHab(request, idHab):
    habitacion = Habitacion.objects.get(idHab = idHab)
    tipoHabs = tipoHab.objects.all()
    capturas = imgHab.objects.filter(idHab=habitacion)
    servicios = servicio.objects.all()
    disponibilidad = dispHab.objects.all()
    urlCapturas = ""
    for i in capturas:
        urlCapturas += i.imagen.url + " "
    context = {
    'habitacion': habitacion,
    'tipoHabs': tipoHabs,
    'servicios': servicios,
    'disponibilidad': disponibilidad,
    'capturas' : capturas,
    'urlCapturas' : urlCapturas
    }
    return render(request, 'registroHab.html', context)


#series:

@login_required
def listadoReservas(request):
    context = {}
    reservas = Reserva.objects.all()
    print("---------")
    print(reservas)
    context['reservas'] = reservas
    return render(request, 'listadoReservas.html', context)

@login_required
def eliminarReserva(request, idReserva):
    context = {}
    try:
        reserva = Reserva.objects.get(idReserva = idReserva)
        reserva.delete()
        context['exito'] = 'Reserva eliminada con éxito'
    except:
        context['error'] = 'Error al eliminar la reserva'
    
    reservas = Reserva.objects.all()
    context['reservas'] = reservas
    return render(request, 'listadoReservas.html', context)

@login_required
def subirReserva(request):
    context = {}
    if request.method == 'POST':
        
        idReserva       = request.POST['txtId']
        fecha           = request.POST['fechaReserva1']
        dias            = request.POST['cantidadDias']
       
        #convertir idserie en un string para comparar
        str(idReserva)
        if 'enviarReserva' in request.POST:
            if idReserva == "0":
                 Reserva.objects.create(
                    fecha = fecha,
                    dias = dias,
                    habitacion = Habitacion.objects.get(idHab=request.POST['habitacion'])
                    )
                 context['exito'] = "Reserva creada con éxito"
            else:
                reserva = Reserva.objects.get(idReserva = request.POST['txtId'])
                reserva.fecha = fecha
                reserva.dias = dias
                reserva.habitacion = Habitacion.objects.get(idHab=request.POST['habitacion'])
                reserva.save()
                context['exito'] = "Reserva actualizada con éxito"
                
    context['reservas'] = Reserva.objects.all()
    return render(request, 'listadoReservas.html', context)

@login_required
def modificarReserva(request, idReserva):
    reserva = Reserva.objects.get(idReserva = idReserva)
    habitaciones = Habitacion.objects.all()
    context = {
    'reserva': reserva,
    'habitaciones': habitaciones,
    }
    return render(request, 'registroReservas.html', context)

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





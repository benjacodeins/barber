from datetime import datetime, timedelta, time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import Barbero, Servicio, Turno
from .forms import TurnoForm


# Configuración de horarios de trabajo
HORA_APERTURA = time(9, 0)   # 9:00 AM
HORA_CIERRE = time(19, 0)    # 7:00 PM
INTERVALO_MINUTOS = 30       # Intervalos de 30 minutos para la grilla


def landing(request):
    """Vista principal que muestra servicios y barberos."""
    servicios = Servicio.objects.all()
    barberos = Barbero.objects.filter(activo=True)
    
    context = {
        'servicios': servicios,
        'barberos': barberos,
    }
    return render(request, 'reservas/landing.html', context)


def reservar(request):
    """Vista del formulario de reserva."""
    form = TurnoForm()
    servicios = Servicio.objects.all()
    barberos = Barbero.objects.filter(activo=True)
    
    # Fecha mínima: hoy
    fecha_minima = datetime.now().date().isoformat()
    
    context = {
        'form': form,
        'servicios': servicios,
        'barberos': barberos,
        'fecha_minima': fecha_minima,
    }
    return render(request, 'reservas/reservar.html', context)


def generar_slots_disponibles(barbero, servicio, fecha):
    """
    Genera los slots de tiempo disponibles para un barbero en una fecha específica.
    Tiene en cuenta la duración del servicio seleccionado.
    """
    slots = []
    duracion_servicio = timedelta(minutes=servicio.duracion_minutos)
    
    # Obtener todos los turnos del barbero para esa fecha
    inicio_dia = timezone.make_aware(datetime.combine(fecha, HORA_APERTURA))
    fin_dia = timezone.make_aware(datetime.combine(fecha, HORA_CIERRE))
    
    turnos_existentes = Turno.objects.filter(
        barbero=barbero,
        fecha_hora_inicio__date=fecha,
        estado__in=['pendiente', 'confirmado']
    ).order_by('fecha_hora_inicio')
    
    # Crear lista de intervalos ocupados
    ocupados = [(t.fecha_hora_inicio, t.fecha_hora_fin) for t in turnos_existentes]
    
    # Generar slots desde la apertura hasta el cierre
    slot_actual = inicio_dia
    
    # Si la fecha es hoy, empezamos desde la próxima hora disponible
    ahora = timezone.now()
    if fecha == ahora.date():
        # Redondear al siguiente intervalo de 30 minutos
        minutos = ((ahora.minute // INTERVALO_MINUTOS) + 1) * INTERVALO_MINUTOS
        if minutos >= 60:
            slot_actual = ahora.replace(hour=ahora.hour + 1, minute=0, second=0, microsecond=0)
        else:
            slot_actual = ahora.replace(minute=minutos, second=0, microsecond=0)
        
        if slot_actual < inicio_dia:
            slot_actual = inicio_dia
    
    while slot_actual + duracion_servicio <= fin_dia:
        slot_fin = slot_actual + duracion_servicio
        
        # Verificar si el slot está libre (no hay overlap con turnos existentes)
        slot_libre = True
        for ocupado_inicio, ocupado_fin in ocupados:
            # Hay overlap si el slot comienza antes de que termine el ocupado
            # Y termina después de que comience el ocupado
            if slot_actual < ocupado_fin and slot_fin > ocupado_inicio:
                slot_libre = False
                break
        
        if slot_libre:
            slots.append({
                'inicio': slot_actual,
                'fin': slot_fin,
                'hora_display': slot_actual.strftime('%H:%M'),
            })
        
        # Avanzar al siguiente intervalo
        slot_actual += timedelta(minutes=INTERVALO_MINUTOS)
    
    return slots


@require_GET
def obtener_horarios_disponibles(request):
    """
    Vista HTMX que devuelve los horarios disponibles como HTML parcial.
    Recibe: barbero_id, servicio_id, fecha
    """
    barbero_id = request.GET.get('barbero')
    servicio_id = request.GET.get('servicio')
    fecha_str = request.GET.get('fecha')
    
    # Validar que todos los campos estén presentes
    if not all([barbero_id, servicio_id, fecha_str]):
        return HttpResponse(
            '<p class="text-muted">Selecciona un barbero, servicio y fecha para ver los horarios disponibles.</p>'
        )
    
    try:
        barbero = get_object_or_404(Barbero, id=barbero_id, activo=True)
        servicio = get_object_or_404(Servicio, id=servicio_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return HttpResponse(
            '<p class="text-danger">Error en los datos proporcionados.</p>'
        )
    
    # No permitir fechas pasadas
    if fecha < datetime.now().date():
        return HttpResponse(
            '<p class="text-warning">No puedes reservar en fechas pasadas.</p>'
        )
    
    # Generar slots disponibles
    slots = generar_slots_disponibles(barbero, servicio, fecha)
    
    if not slots:
        return HttpResponse(
            '<p class="text-warning">No hay horarios disponibles para esta fecha. Prueba con otra fecha.</p>'
        )
    
    context = {
        'slots': slots,
        'barbero': barbero,
        'servicio': servicio,
        'fecha': fecha,
    }
    return render(request, 'reservas/partials/_horarios_disponibles.html', context)


@require_POST
@transaction.atomic
def guardar_turno(request):
    """
    Guarda un nuevo turno con prevención de concurrencia.
    Usa transaction.atomic y select_for_update para evitar doble reserva.
    """
    barbero_id = request.POST.get('barbero_id')
    servicio_id = request.POST.get('servicio_id')
    fecha_hora_str = request.POST.get('fecha_hora')
    nombre_cliente = request.POST.get('nombre_cliente')
    whatsapp_cliente = request.POST.get('whatsapp_cliente')
    
    # Validaciones básicas
    if not all([barbero_id, servicio_id, fecha_hora_str, nombre_cliente, whatsapp_cliente]):
        messages.error(request, 'Todos los campos son obligatorios.')
        return redirect('reservas:reservar')
    
    try:
        barbero = Barbero.objects.select_for_update().get(id=barbero_id, activo=True)
        servicio = Servicio.objects.get(id=servicio_id)
        fecha_hora_inicio = datetime.fromisoformat(fecha_hora_str)
    except (Barbero.DoesNotExist, Servicio.DoesNotExist, ValueError):
        messages.error(request, 'Error en los datos de la reserva.')
        return redirect('reservas:reservar')
    
    # Calcular hora de fin
    duracion = timedelta(minutes=servicio.duracion_minutos)
    fecha_hora_fin = fecha_hora_inicio + duracion
    
    # Verificar nuevamente disponibilidad dentro de la transacción (prevención de concurrencia)
    turnos_conflicto = Turno.objects.filter(
        barbero=barbero,
        estado__in=['pendiente', 'confirmado']
    ).filter(
        Q(fecha_hora_inicio__lt=fecha_hora_fin) & Q(fecha_hora_fin__gt=fecha_hora_inicio)
    )
    
    if turnos_conflicto.exists():
        messages.error(
            request, 
            '¡Lo sentimos! Este horario acaba de ser reservado por otro cliente. Por favor, elige otro horario.'
        )
        return redirect('reservas:reservar')
    
    # Crear el turno
    turno = Turno.objects.create(
        barbero=barbero,
        servicio=servicio,
        fecha_hora_inicio=fecha_hora_inicio,
        fecha_hora_fin=fecha_hora_fin,
        nombre_cliente=nombre_cliente,
        whatsapp_cliente=whatsapp_cliente,
        estado='pendiente'
    )
    
    messages.success(
        request, 
        f'¡Turno reservado con éxito! Te esperamos el {turno.fecha_hora_inicio.strftime("%d/%m/%Y a las %H:%M")}.'
    )
    return render(request, 'reservas/partials/_confirmacion.html', {'turno': turno})


# ============================================
# PANEL DE ADMINISTRACIÓN
# ============================================

def panel_login(request):
    """Vista de login personalizada para el panel."""
    if request.user.is_authenticated:
        return redirect('reservas:panel')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('reservas:panel')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'panel/login.html')


def panel_logout(request):
    """Cierra la sesión del usuario."""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('reservas:panel_login')


@login_required(login_url='reservas:panel_login')
def panel_dashboard(request):
    """Dashboard principal del panel de administración."""
    # Filtros
    estado_filtro = request.GET.get('estado', 'pendiente')
    fecha_filtro = request.GET.get('fecha', '')
    
    # Query base
    turnos = Turno.objects.select_related('barbero', 'servicio')
    
    # Aplicar filtro de estado
    if estado_filtro and estado_filtro != 'todos':
        turnos = turnos.filter(estado=estado_filtro)
    
    # Aplicar filtro de fecha
    if fecha_filtro:
        try:
            fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
            turnos = turnos.filter(fecha_hora_inicio__date=fecha)
        except ValueError:
            pass
    
    # Ordenar por fecha
    turnos = turnos.order_by('fecha_hora_inicio')
    
    # Contadores para badges
    contadores = {
        'pendientes': Turno.objects.filter(estado='pendiente').count(),
        'confirmados': Turno.objects.filter(estado='confirmado').count(),
        'cancelados': Turno.objects.filter(estado='cancelado').count(),
    }
    
    context = {
        'turnos': turnos,
        'estado_filtro': estado_filtro,
        'fecha_filtro': fecha_filtro,
        'contadores': contadores,
        'hoy': timezone.now().date().isoformat(),
    }
    return render(request, 'panel/dashboard.html', context)


@login_required(login_url='reservas:panel_login')
@require_POST
def cambiar_estado_turno(request, turno_id):
    """Cambia el estado de un turno (confirmar/cancelar)."""
    turno = get_object_or_404(Turno, id=turno_id)
    nuevo_estado = request.POST.get('estado')
    
    if nuevo_estado in ['confirmado', 'cancelado', 'pendiente']:
        turno.estado = nuevo_estado
        turno.save()
        
        estado_display = dict(Turno.ESTADO_CHOICES).get(nuevo_estado, nuevo_estado)
        messages.success(request, f'Turno de {turno.nombre_cliente} marcado como {estado_display}.')
    
    # Si es petición HTMX, devolver solo la fila actualizada
    if request.headers.get('HX-Request'):
        return render(request, 'panel/partials/_turno_row.html', {'turno': turno})
    
    return redirect('reservas:panel')

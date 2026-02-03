from django.contrib import admin
from .models import Barbero, Servicio, Turno


@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'especialidad', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'especialidad']


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'duracion_minutos', 'es_premium']
    list_filter = ['es_premium']
    search_fields = ['nombre']


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['nombre_cliente', 'barbero', 'servicio', 'fecha_hora_inicio', 'estado']
    list_filter = ['estado', 'barbero', 'fecha_hora_inicio']
    search_fields = ['nombre_cliente', 'whatsapp_cliente']
    date_hierarchy = 'fecha_hora_inicio'
    readonly_fields = ['creado_en']

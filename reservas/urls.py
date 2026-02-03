from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('reservar/', views.reservar, name='reservar'),
    path('horarios/', views.obtener_horarios_disponibles, name='horarios'),
    path('guardar/', views.guardar_turno, name='guardar'),
    
    # Panel de Administración
    path('panel/', views.panel_dashboard, name='panel'),
    path('panel/login/', views.panel_login, name='panel_login'),
    path('panel/logout/', views.panel_logout, name='panel_logout'),
    path('panel/turno/<int:turno_id>/estado/', views.cambiar_estado_turno, name='cambiar_estado'),
]

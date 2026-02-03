from django.db import models


class Barbero(models.Model):
    """Modelo para los profesionales de la peluquería/barbería."""
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='barberos/', blank=True, null=True)
    especialidad = models.CharField(max_length=150, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Barbero'
        verbose_name_plural = 'Barberos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    """Modelo para los servicios ofrecidos."""
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(
        help_text='Duración del servicio en minutos'
    )
    es_premium = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Turno(models.Model):
    """Modelo para las reservas de turnos."""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    barbero = models.ForeignKey(
        Barbero,
        on_delete=models.CASCADE,
        related_name='turnos'
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='turnos'
    )
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    nombre_cliente = models.CharField(max_length=150)
    whatsapp_cliente = models.CharField(max_length=20)
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Turno'
        verbose_name_plural = 'Turnos'
        ordering = ['-fecha_hora_inicio']

    def __str__(self):
        return f"{self.nombre_cliente} - {self.barbero.nombre} ({self.fecha_hora_inicio.strftime('%d/%m/%Y %H:%M')})"

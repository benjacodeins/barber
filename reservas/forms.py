from django import forms
from .models import Turno


class TurnoForm(forms.ModelForm):
    """Formulario para crear una reserva de turno."""
    
    class Meta:
        model = Turno
        fields = ['barbero', 'servicio', 'nombre_cliente', 'whatsapp_cliente']
        widgets = {
            'barbero': forms.Select(attrs={
                'class': 'form-select',
                'hx-get': '/reservas/horarios/',
                'hx-target': '#horarios-container',
                'hx-include': '[name="servicio"], [name="fecha"]',
                'hx-trigger': 'change',
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-select',
                'hx-get': '/reservas/horarios/',
                'hx-target': '#horarios-container',
                'hx-include': '[name="barbero"], [name="fecha"]',
                'hx-trigger': 'change',
            }),
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
            }),
            'whatsapp_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: +54 9 11 1234-5678',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['barbero'].queryset = self.fields['barbero'].queryset.filter(activo=True)
        self.fields['barbero'].empty_label = 'Selecciona un barbero'
        self.fields['servicio'].empty_label = 'Selecciona un servicio'


class BuscarHorariosForm(forms.Form):
    """Formulario para buscar horarios disponibles."""
    barbero = forms.IntegerField(widget=forms.HiddenInput())
    servicio = forms.IntegerField(widget=forms.HiddenInput())
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'hx-get': '/reservas/horarios/',
            'hx-target': '#horarios-container',
            'hx-include': '[name="barbero"], [name="servicio"]',
            'hx-trigger': 'change',
        })
    )

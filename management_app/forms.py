from django import forms
from .models import Encomienda

class EncomiendaForm(forms.ModelForm):
    class Meta:
        model = Encomienda
        fields = ['Fecha_Llegada', 'Departamento', 'Residente', 'Fecha_Recepcion', 'Estado']
        widgets = {
            'Fecha_Llegada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'Fecha_Recepcion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    # Ajustar formatos para compatibilidad con el navegador
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['Fecha_Llegada', 'Fecha_Recepcion']:
            self.fields[field].input_formats = ['%Y-%m-%dT%H:%M']


from django import forms
from .models import TipoPrestamo, Prestamo

class TipoPrestamoForm(forms.ModelForm):
    class Meta:
        model = TipoPrestamo
        fields = '__all__'
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'tasa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['empleado', 'tipo_prestamo', 'fecha_prestamo', 'monto', 'numero_cuotas']
        widgets = {
            'fecha_prestamo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'tipo_prestamo': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
            'numero_cuotas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
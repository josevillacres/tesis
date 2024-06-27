from django import forms # type: ignore
from .models import *

class MedicoForm(forms.ModelForm):
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Medico
        fields = ['cedula', 'nombre1', 'nombre2', 'apellido1', 'apellido2', 'celular', 'email', 'direccion', 'especialidad']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre1': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre2': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido1': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido2': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'] = forms.ModelChoiceField(queryset=Usuario.objects.all(), widget=forms.HiddenInput())
        self.fields['contrasena'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get("contrasena")
        confirmar_contrasena = cleaned_data.get("confirmar_contrasena")

        if contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data
    

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cedula', 'nombre1', 'nombre2', 'apellido1', 'apellido2', 
                  'fecha_nacimiento', 'genero', 'celular', 'email', 
                  'direccion', 'ocupacion', 'tipo_sangre']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'genero': forms.Select(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]),
        }



class RegistroMedicoForm(forms.ModelForm):
    class Meta:
        model = RegistroMedico
        fields = ['paciente', 'medico', 'fecha_registro_medico', 'razon']

class SignosVitalesForm(forms.ModelForm):
    class Meta:
        model = SignosVitales
        fields = ['presion', 'temperatura', 'talla', 'peso', 'imc']

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['enfermedad', 'descripcion', 'fecha_diagnostico']

class PrescripcionMedicaForm(forms.ModelForm):
    class Meta:
        model = PrescripcionMedica
        fields = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones']



# forms.py
from .models import RegistroMedico, SignosVitales, Diagnostico, PrescripcionMedica

class RegistroMedicoForm(forms.ModelForm):
    class Meta:
        model = RegistroMedico
        fields = ['fecha_registro_medico', 'razon']
        widgets = {
            'fecha_registro_medico': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'razon': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SignosVitalesForm(forms.ModelForm):
    class Meta:
        model = SignosVitales
        fields = ['presion', 'temperatura', 'talla', 'peso', 'imc']
        widgets = {
            'presion': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '7'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'talla': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'imc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['enfermedad', 'descripcion', 'fecha_diagnostico']
        widgets = {
            'enfermedad': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_diagnostico': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

class PrescripcionMedicaForm(forms.ModelForm):
    class Meta:
        model = PrescripcionMedica
        fields = ['medicamento', 'dosis', 'frecuencia', 'duracion', 'instrucciones']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-control'}),
            'dosis': forms.TextInput(attrs={'class': 'form-control'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control'}),
            'instrucciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

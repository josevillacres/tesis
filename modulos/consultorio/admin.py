from django.contrib import admin
from modulos.consultorio.models import *
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(TipoSangre)
admin.site.register(Paciente)
admin.site.register(AntecedentesPersonales)
admin.site.register(AntecedentesFamiliares)
admin.site.register(Alergias)
admin.site.register(Traumas)
admin.site.register(Habitos)
admin.site.register(AntecedenteClinico)
admin.site.register(TipoEnfermedad)
admin.site.register(Enfermedad)
admin.site.register(RegistroMedico)
admin.site.register(SignosVitales)
admin.site.register(Diagnostico)
admin.site.register(Medicamento)
admin.site.register(PrescripcionMedica)
admin.site.register(EnvioPrescripcion)

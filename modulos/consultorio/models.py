from django.db import models # type: ignore

# modelo usuario
class Usuario(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=25) 

    def __str__(self):
        return self.email

# modelo especialidad
class Especialidad(models.Model):
    especialidad = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.especialidad

# modelo medico
class Medico(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, blank=True, null=True)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    direccion = models.CharField(max_length=50)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre1} {self.apellido1}"

# modelo tipo de sangre
class TipoSangre(models.Model):
    sangre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.sangre

# modelo paciente
class Paciente(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50, blank=True, null=True)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    celular = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    direccion = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=50)
    tipo_sangre = models.ForeignKey(TipoSangre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre1} {self.apellido1}"

# modelo antecedentes personales
class AntecedentesPersonales(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)

# modelo antecedentes familiares
class AntecedentesFamiliares(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    relacion = models.CharField(max_length=50)

# modelo alergias
class Alergias(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)

# modelo traumas
class Traumas(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)

# modelo habitso
class Habitos(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

# modelo antecedentes clinicos
class AntecedenteClinico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255)
    fecha = models.DateTimeField(blank=True, null=True)

# modelo tipos de enfermedad
class TipoEnfermedad(models.Model):
    codigo = models.CharField(max_length=50)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

# modelo enfermedad
class Enfermedad(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=255)
    tipo_enfermedad = models.ForeignKey(TipoEnfermedad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

# Modelo RegistroMedico
class RegistroMedico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_registro_medico = models.DateTimeField()
    razon = models.CharField(max_length=255)

    def __str__(self):
        return f"Registro Médico de {self.paciente} por {self.medico}"

# modelo signos vitales
class SignosVitales(models.Model):
    registro_medico = models.OneToOneField(RegistroMedico, on_delete=models.CASCADE)
    presion = models.CharField(max_length=7, blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    talla = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    peso = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    imc = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f"Signos Vitales de {self.registro_medico}"

# modelo diagnostico
class Diagnostico(models.Model):
    registro_medico = models.ForeignKey(RegistroMedico, on_delete=models.CASCADE)
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecha_diagnostico = models.DateTimeField()
    
    def __str__(self):
        return f"Diagnóstico de {self.enfermedad} en {self.registro_medico}"

# modelo medicamento
class Medicamento(models.Model):
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=255)
    forma_farmaceutica = models.CharField(max_length=255)
    concentracion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# modelo prescripcion medica
class PrescripcionMedica(models.Model):
    registro_medico = models.ForeignKey(RegistroMedico, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50, blank=True, null=True)
    duracion = models.CharField(max_length=50, blank=True, null=True)
    instrucciones = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Prescripción de {self.medicamento} en {self.registro_medico}"

# modelo envio prescripcion medica
class EnvioPrescripcion(models.Model):
    prescripcion = models.OneToOneField(PrescripcionMedica, on_delete=models.CASCADE)
    metodo_envio = models.CharField(max_length=50, blank=True, null=True)
    estado_envio = models.CharField(max_length=1, blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
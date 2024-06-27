from django.shortcuts import render, get_object_or_404, redirect # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from .models import *
from .forms import *
from django.urls import reverse_lazy # type: ignore

# vista login
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('pacientes')
        else:
            error_message = "Credenciales inválidas"
            return render(request, 'consultorio/login.html', {'error_message': error_message})
    return render(request, 'consultorio/login.html')

# listar medicos
def listar_medicos(request):
    if not request.user.is_authenticated:
        return redirect('login')
    medicos = Medico.objects.all()
    return render(request, 'consultorio/medicos.html',{'medicos': medicos})

# agregar medico
def agregar_medico(request):
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_medicos')  
    else:
        form = MedicoForm()
    return render(request, 'consultorio/agregar_medico.html', {'form': form})

# editar medico
def editar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medicos')  
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'consultorio/editar_medico.html', {'form': form})

# eliminar medico
def eliminar_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == 'POST':
        medico.delete()
        return redirect('medicos') 
    return render(request, 'consultorio/confirmar_eliminar_medico.html', {'medico': medico})

# listar pacientes
def listar_pacientes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pacientes = Paciente.objects.all()
    return render(request, 'consultorio/pacientes.html',{'pacientes': pacientes})

# crear paciente
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'consultorio/paciente_form.html', {'form': form})

# crear modificar
def modificar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'consultorio/paciente_form.html', {'form': form})

# crear eliminar
def eliminar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    if request.method == 'POST':
        paciente.delete()
        return redirect('lista_pacientes')
    return render(request, 'consultorio/paciente_eliminar.html', {'paciente': paciente})

##########################################
# ficha medica
def ficha_medica(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)
    antecedentes_personales = AntecedentesPersonales.objects.filter(paciente=paciente)
    antecedentes_familiares = AntecedentesFamiliares.objects.filter(paciente=paciente)
    alergias = Alergias.objects.filter(paciente=paciente)
    traumas = Traumas.objects.filter(paciente=paciente)
    habitos = Habitos.objects.filter(paciente=paciente)
    registros_medicos = RegistroMedico.objects.filter(paciente=paciente)
    diagnosticos = Diagnostico.objects.filter(registro_medico__paciente=paciente)
    prescripciones = PrescripcionMedica.objects.filter(registro_medico__paciente=paciente)
    
    context = {
        'paciente': paciente,
        'antecedentes_personales': antecedentes_personales,
        'antecedentes_familiares': antecedentes_familiares,
        'alergias': alergias,
        'traumas': traumas,
        'habitos': habitos,
        'registros_medicos': registros_medicos,
        'diagnosticos': diagnosticos,
        'prescripciones': prescripciones,
    }
    return render(request, 'consultorio/ficha_medica.html', context)


# generador de prescripcion medica
def generar_consulta_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method == 'POST':
        registro_form = RegistroMedicoForm(request.POST)
        signos_form = SignosVitalesForm(request.POST)
        diagnostico_form = DiagnosticoForm(request.POST)
        prescripcion_form = PrescripcionMedicaForm(request.POST)

        if registro_form.is_valid() and signos_form.is_valid() and diagnostico_form.is_valid() and prescripcion_form.is_valid():
            registro = registro_form.save(commit=False)
            registro.paciente = paciente
            registro.save()

            signos_form.instance.registro_medico = registro
            signos_form.save()

            diagnostico_form.instance.registro_medico = registro
            diagnostico_form.save()

            prescripcion_form.instance.registro_medico = registro
            prescripcion_form.save()

            return redirect('lista_pacientes') 

    else:
        registro_form = RegistroMedicoForm()
        signos_form = SignosVitalesForm()
        diagnostico_form = DiagnosticoForm()
        prescripcion_form = PrescripcionMedicaForm()

    context = {
        'registro_form': registro_form,
        'signos_form': signos_form,
        'diagnostico_form': diagnostico_form,
        'prescripcion_form': prescripcion_form,
        'paciente': paciente,
    }

    return render(request, 'consultorio/generar_consulta_paciente.html', context)


# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import RegistroMedico, Paciente
from .forms import RegistroMedicoForm, SignosVitalesForm, DiagnosticoForm, PrescripcionMedicaForm
import qrcode
import io


def guardar_consulta(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)

    if request.method == 'POST':
        registro_form = RegistroMedicoForm(request.POST)
        signos_form = SignosVitalesForm(request.POST)
        diagnostico_form = DiagnosticoForm(request.POST)
        prescripcion_form = PrescripcionMedicaForm(request.POST)

        if registro_form.is_valid() and signos_form.is_valid() and diagnostico_form.is_valid() and prescripcion_form.is_valid():
            # Guardar el formulario de RegistroMedico
            registro_medico = registro_form.save(commit=False)
            registro_medico.paciente = paciente
            registro_medico.save()

            # Guardar el formulario de SignosVitales
            signos_vitales = signos_form.save(commit=False)
            signos_vitales.registro_medico = registro_medico
            signos_vitales.save()

            # Guardar el formulario de Diagnostico
            diagnostico = diagnostico_form.save(commit=False)
            diagnostico.registro_medico = registro_medico
            diagnostico.save()

            # Guardar el formulario de PrescripcionMedica
            prescripcion = prescripcion_form.save(commit=False)
            prescripcion.registro_medico = registro_medico
            prescripcion.save()
            qr_code = generate_qr_code(registro_medico.medico) # type: ignore
            # Obtener los datos relevantes para el correo electrónico
            medico = registro_medico.medico
            consultorio = "DuoMedic"  
            firma_electronica = qr_code

            # Preparar el contenido del correo electrónico
            subject = f"Consulta Médica para {paciente.nombre1} {paciente.apellido1}"
            context = {
                'paciente': paciente,
                'medico': medico,
                'consultorio': consultorio,
                'firma_electronica': firma_electronica,
                'diagnostico': diagnostico,
                'prescripcion': prescripcion,
            }
            html_message = render_to_string('consultorio/consulta_medica.html', context)
            plain_message = strip_tags(html_message)  # Eliminar etiquetas HTML para versión de texto plano

            # Enviar correo electrónico
            send_mail(subject, plain_message, 'consultorio.duomedic.ambato@gmail.com', [paciente.email], html_message=html_message)

            return redirect('ruta_de_redireccion')  # Redirigir a la página deseada después de guardar

    else:
        registro_form = RegistroMedicoForm()
        signos_form = SignosVitalesForm()
        diagnostico_form = DiagnosticoForm()
        prescripcion_form = PrescripcionMedicaForm()

    return render(request, 'consultorio/registro_medico_form.html', {
        'registro_form': registro_form,
        'signos_form': signos_form,
        'diagnostico_form': diagnostico_form,
        'prescripcion_form': prescripcion_form,
        'paciente': paciente,
    })


def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    qr_img.save(buffer)
    return buffer.getvalue()

########################

def reporte_consultas(request):
    # Obtener todos los médicos para el combo box
    medicos = Medico.objects.all()

    # Inicializar variables para gráficos
    datos_consultas_por_mes = []
    datos_consultas_por_dia = []

    # Si se ha enviado el formulario (seleccionado un médico)
    if 'medico' in request.GET:
        medico_id = request.GET['medico']

        # Obtener consultas por mes para el médico seleccionado
        consultas_por_mes = (
            RegistroMedico.objects
            .filter(medico_id=medico_id)
            .annotate(mes=Count('fecha_registro_medico__month'))
            .values('mes')
        )

        # Generar datos para el gráfico de consultas por mes
        datos_consultas_por_mes = [consulta['mes'] for consulta in consultas_por_mes]

        # Obtener consultas por día para el médico seleccionado (ejemplo ficticio)
        # En una aplicación real, esto debería ser más complejo y basado en datos reales
        datos_consultas_por_dia = [8, 5, 12, 9, 4]  # Datos ficticios para demostración

    context = {
        'medicos': medicos,
        'datos_consultas_por_mes': datos_consultas_por_mes,
        'datos_consultas_por_dia': datos_consultas_por_dia,
    }

    return render(request, 'consultorio/reporte_consultas.html', context)


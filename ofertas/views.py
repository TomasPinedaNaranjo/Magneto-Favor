from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import Formulario_Oferta, RatingForm, PaymentForm, CustomPasswordChangeForm
from django.http import HttpResponse
from .models import Ofertas, Rating
import folium
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import logging
from django.db.models import Q
from django.core.mail import EmailMessage

import openai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def eliminar_oferta(request, oferta_id):
    oferta = get_object_or_404(Ofertas, pk=oferta_id)

    # Verificar si el usuario actual es el creador de la oferta
    if oferta.user == request.user:
        oferta.delete()  # Eliminar la oferta
        # Redirigir al usuario a la página de ofertas nuevamente o a donde desees
        return redirect('ofertas')
    else:
        # Manejar el caso en el que el usuario no tiene permiso para eliminar la oferta
        # Puedes mostrar un mensaje de error o redirigirlo a otra página
        # Aquí redirigimos al usuario a la página de ofertas
        return redirect('ofertas')


# Create your views here.
@login_required
def mapa(request):
    locations = Ofertas.objects.all()

    initialMap = folium.Map(location=[6.199939, -75.578608], zoom_start= 20)

    

    for location in locations:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup='Oferta '+ location.title).add_to(initialMap)

    context = {'map':initialMap._repr_html_(), 'locations': locations}    
    return render(request, 'mapa.html', context)

@login_required
def ofertas(request):
    query = request.GET.get("q")
    lista_ofertas = Ofertas.objects.exclude(aceptada=True)

    if query:
        lista_ofertas = lista_ofertas.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'ofertas.html', {'Ofertas': lista_ofertas, 'query': query})

@login_required
def aceptar_oferta(request, oferta_id):
    oferta = get_object_or_404(Ofertas, id=oferta_id)
    
    # Verifica si el usuario actual no es el propietario de la oferta
    if request.user != oferta.user:
        # Marca la oferta como aceptada
        oferta.aceptada = True
        oferta.aceptada_por = request.user  # Registra quién la aceptó
        oferta.save()
        #se llama la funcion
        mandar_email(oferta, request.user)
    
    return redirect('ofertas')

@login_required
def ofertas_en_curso(request):
    ofertas_en_curso = Ofertas.objects.filter(aceptada=True, aceptada_por=request.user, terminada = False)
    
    return render(request, 'ofertas_en_curso.html', {'OfertasEnCurso': ofertas_en_curso})


@login_required
def editar_oferta(request, oferta_id):
    oferta = get_object_or_404(Ofertas, pk=oferta_id)
    
    # Verificar si el usuario actual es el creador de la oferta
    if oferta.user != request.user:
        return redirect('ofertas')  # O a otra página de error

    if request.method == 'POST':
        form = Formulario_Oferta(request.POST, instance=oferta)
        if form.is_valid():
            form.save()
            return redirect('ofertas')  # Redirigir a la lista de ofertas después de la edición
    else:
        form = Formulario_Oferta(instance=oferta)  # Cargar los datos actuales de la oferta en el formulario

    return render(request, 'editar_ofertas.html', {'form': form, 'oferta': oferta})

@login_required
def crear_ofertas(request):
    
    if request.method == 'GET':
        return render(request, 'crear_ofertas.html', {
            'form': Formulario_Oferta 
        })
    else:
        try:
            form = Formulario_Oferta(request.POST)
            nueva_oferta = form.save(commit=False)
            nueva_oferta.user = request.user
            nueva_oferta.save()
            
            return redirect('ofertas')
        except ValueError:
            return render(request, 'crear_ofertas.html', {
                'form': Formulario_Oferta,
                'error' : 'Porfavor ingrese un título y una descripción válidas'
            })

        

# autenticación

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Ese usuario ya existe, intente de nuevo porfavor"})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Las contraseñas no coinciden, intente de nuevo porfavor"})


def home(request):
    return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrectas, intente de nuevo por favor"})

        login(request, user)
        return redirect('home')

@login_required
def cancelar_oferta(request, oferta_id):
    print("Entrando a cancelar_oferta")  # Mensaje de depuración
    oferta = get_object_or_404(Ofertas, pk=oferta_id)

    if oferta.user == request.user or oferta.aceptada_por == request.user:
        print("Usuario correcto")  # Mensaje de depuración
        oferta.aceptada = False
        oferta.aceptada_por = None
        oferta.save()
        
        return redirect('ofertas_en_curso')  # Redirigir a la vista de "ofertas en curso" después de cancelar
    else:
        print("Usuario incorrecto")  # Mensaje de depuración
        # Manejar el caso donde el usuario no tiene permiso para cancelar la oferta
        # Puedes mostrar un mensaje de error o redirigir a otra página
        return redirect('ofertas_en_curso')

# rating 
@login_required
def rate_offer(request, offer_id):
    offer = Ofertas.objects.get(pk=offer_id)
    user = request.user

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            overall_experience = form.cleaned_data['overall_experience']
            would_use_again = form.cleaned_data['would_use_again']
            improvement_suggestions = form.cleaned_data['improvement_suggestions']

            rating, created = Rating.objects.get_or_create(offer=offer, user=user)
            rating.overall_experience = overall_experience
            rating.would_use_again = would_use_again
            rating.improvement_suggestions = improvement_suggestions
            rating.save()

            return redirect('home')
    else:
        form = RatingForm()

    return render(request, 'rate_offer.html', {'offer': offer, 'form': form})
@login_required
def view_ratings(request, offer_id):
    offer = Ofertas.objects.get(pk=offer_id)
    ratings = Rating.objects.filter(offer=offer)

    return render(request, 'view_ratings.html', {'offer': offer, 'ratings': ratings})


@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('home')  # Cambia 'home' a la URL de la página de inicio de tu aplicación
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'edit_user.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión del usuario para evitar que se cierre la sesión
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('home')  # Cambia 'home' a la URL de la página de inicio de tu aplicación
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})



@login_required
def servicio_terminado(request, oferta_id):
    oferta = get_object_or_404(Ofertas, pk=oferta_id)

    # Verificar si el usuario actual es el trabajador que aceptó la oferta
    if oferta.aceptada_por == request.user:
        oferta.terminada = True
        oferta.fecha_terminacion = timezone.now()  # Establecer la fecha de terminación
        oferta.save()


    return redirect('ofertas_en_curso')


@login_required
def servicios_terminados(request):
    servicios_realizados = Ofertas.objects.filter(terminada=True, aceptada_por=request.user)
    
    return render(request, 'servicios_terminados.html', {'ServiciosRealizados': servicios_realizados})

@login_required
def pasarela_pago(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Procesar la información de pago (simulación)
            amount = form.cleaned_data['amount']
            # Realiza aquí la lógica de procesamiento de pago (puede ser una simulación)
            # Asegúrate de manejar la información de pago de manera segura en una aplicación real.

            return render(request, 'pago_exitoso.html', {'amount': amount})
    else:
        form = PaymentForm()

    return render(request, 'formulario_pago.html', {'form': form})


#mandar email de oferta aceptada
def mandar_email(oferta, usuario_que_acepto):
    subject = "Acaban de aceptar tu oferta de trabajo!"
    message = f"¡Felicidades! Tu oferta de trabajo titulada '{oferta.title}' ha sido aceptada por {usuario_que_acepto.username}. Puedes ponerte en contacto con el prestador mediante su correo ({usuario_que_acepto.email}) para continuar el proceso."
    from_email = "tu_correo@gmail.com"  # Cambia esto al correo del remitente
    recipient_list = [oferta.user.email]  # Utiliza la dirección de correo electrónico del propietario de la oferta
    email = EmailMessage(subject, message, from_email, recipient_list)
    
    try:
        email.send()
    except Exception as e:
        # Maneja cualquier error que pueda ocurrir al enviar el correo electrónico
        # Puedes registrar el error en los registros de tu aplicación o manejarlo de otra manera
        pass
    

#implementar chatgpt


# Retrieve the OpenAI API key from the environment variables
openai.api_key = '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'

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    user_messages = [{'role': msg['role'], 'content': msg['content']} for msg in messages if msg['role'] == 'user']
    assistant_messages = [{'role': msg['role'], 'content': msg['content']} for msg in messages if msg['role'] == 'assistant']

    prompt = ""
    for msg in user_messages:
        prompt += f"{msg['content']}\n"

    # Add the assistant's messages to the prompt
    for msg in assistant_messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=150,  # Adjust as needed
    )

    return response.choices[0].text.strip()
def collect_messages(prompt, context):
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    print(f"Asistente: {response}")
    return response


context = [{'role': 'system', 'content': """
    Eres un asistente virtual de MagnetoFavor tu labor es resolver dudas a los usuarios sobre la plataforma/
    Primero saludas al usuario y te ofreces a solucionar inquietudes/
    El contexto de la plataforma MagnetoFavor es una plataforma web que le permite a los usuario publicar ofertas de trabajos informales como meseros, pintores, carpinteros, paseadores de perros, manicuristas entre otros. Y también permite la contratación de estos mismos servicios, importante que sea en español/
    El funcionamiento de la plataforma es el siguiente, se registran y tienen las siguientes opciones en la barra de navegación/
    Ofertas: Acá se visualizan las ofertas publicadas y puede usar un buscador para filtrar ofertas por las necesidades correspondientes/
    Mapa: Permite ver las ofertas publicadas en la zona/
    Ofertas en Curso: Es la opción que muestra las ofertas tomadas por el usuario/
    Servicios terminados: Es el historial de los servicios finalizados tiene la opción de calificar el servicio y pagar este mismo/
    Crear Oferta: Aquí los que deseen prestar sus servicios pueden publicarlos/
    Mi perfil: En esta opción pueden modificar, actualizar su información personal/
    ¿Por qué elegir MagnetoFavor para publicar tus ofertas?/
    Alcance y Visibilidad: MagnetoFavor cuenta con una base de usuarios activos en busca de servicios de calidad. Publicar tus ofertas aquí te brindará una amplia visibilidad y la oportunidad de llegar a nuevos clientes./
    Facilidad de Uso: Nuestra plataforma es intuitiva y fácil de usar. Publicar tus ofertas es un proceso sencillo, lo que te permite centrarte en lo que haces mejor: brindar servicios excepcionales./
    Comunidad Confiable: En MagnetoFavor, valoramos la confianza y la seguridad. Nuestra comunidad está formada por usuarios verificados y comprometidos./
    """}]

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        if user_input.lower() == 'terminar':
            response_data = {'response': 'Conversación Finalizada.'}
        else:
            collect_messages(user_input, context)
            response_data = {'response': context[-1]['content']}
        return JsonResponse(response_data)
    elif request.method == 'GET':
        # Manejar la solicitud GET para la página principal o el chat inicial
        return render(request, 'chat.html', {})
    else:
        # Manejar otros tipos de solicitudes (opcional)
        return HttpResponse(status=405)  # Método no permitido
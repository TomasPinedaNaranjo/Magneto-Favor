from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import Formulario_Oferta
from django.http import HttpResponse
from .models import Ofertas
import folium

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

def mapa(request):
    locations = Ofertas.objects.all()

    initialMap = folium.Map(location=[6.199939, -75.578608], zoom_start= 20)

    

    for location in locations:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup='Oferta '+ location.title).add_to(initialMap)

    context = {'map':initialMap._repr_html_(), 'locations': locations}    
    return render(request, 'mapa.html', context)

def ofertas(request):
    lista_ofertas = Ofertas.objects.all()
    # si deseo que solo pueda ver las ofertas cierto grupo
    # lista_ofertas = Ofertas.objects.filter(user=request.user)
    return render(request, 'ofertas.html', {'Ofertas': lista_ofertas})

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

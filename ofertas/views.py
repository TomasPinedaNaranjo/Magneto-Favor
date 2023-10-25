from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import Formulario_Oferta, RatingForm
from django.http import HttpResponse
from .models import Ofertas, Rating

# Create your views here.

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

            return redirect('view_rating', offer_id=offer_id)
    else:
        form = RatingForm()

    return render(request, 'rate_offer.html', {'offer': offer, 'form': form})
@login_required
def view_ratings(request, offer_id):
    offer = Ofertas.objects.get(pk=offer_id)
    ratings = Rating.objects.filter(offer=offer)

    return render(request, 'view_ratings.html', {'offer': offer, 'ratings': ratings})

def ver_oferta(request, oferta_id):
    oferta = get_object_or_404(Ofertas, pk=oferta_id)
    return render(request, 'ver_oferta.html', {'oferta': oferta})
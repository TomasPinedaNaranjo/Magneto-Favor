from django.forms import ModelForm
from .models import Ofertas
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm 
from django.contrib.auth import get_user_model

class Formulario_Oferta(ModelForm):
    class Meta:
        model = Ofertas
        fields = ['title', 'description', 'lat', 'lng']
        

#calificación
class RatingForm(forms.Form):
    overall_experience = forms.ChoiceField(
        label="¿Cómo calificarías tu experiencia general con el servicio?",
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect,
    )
    would_use_again = forms.ChoiceField(
        label="¿Volverías a pedir servicio con esta persona?",
        choices=[("SI", "SI"), ("NO", "NO")],
        widget=forms.RadioSelect,
    )
    improvement_suggestions = forms.CharField(
        label="Recomendaciones para mejorar el servicio",
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,  # Opcional
    )
    
#modificar usuario

User = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User  # Utiliza el modelo de usuario predeterminado de Django
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User  # Utiliza el modelo de usuario predeterminado de Django
        
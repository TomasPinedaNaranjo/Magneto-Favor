from django.forms import ModelForm
from .models import Ofertas
from django import forms
#ofertas
class Formulario_Oferta(ModelForm):
    class Meta:
        model = Ofertas
        fields = ['title', 'description']
        

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

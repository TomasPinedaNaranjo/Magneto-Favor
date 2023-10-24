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
    rating = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect,
    )

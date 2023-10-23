from django.forms import ModelForm
from .models import Ofertas

class Formulario_Oferta(ModelForm):
    class Meta:
        model = Ofertas
        fields = ['title', 'description']
        


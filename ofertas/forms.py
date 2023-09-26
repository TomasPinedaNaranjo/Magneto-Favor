from django.forms import ModelForm
from .models import Ofertas

class Formulatio_Oferta(ModelForm):
    class Meta:
        model = Ofertas
        fields = ['title', 'description']
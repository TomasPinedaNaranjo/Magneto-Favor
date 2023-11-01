from django.db import models
from django.contrib.auth.models import User


class Ofertas(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ofertas_creadas')
    lat = models.FloatField()
    lng = models.FloatField()
    aceptada = models.BooleanField(default=False)
    aceptada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ofertas_aceptadas')

    
    class Meta:
        verbose_name_plural = "Ofertas"
    def __str__(self):
        return self.title + '- by ' + self.user.username
   


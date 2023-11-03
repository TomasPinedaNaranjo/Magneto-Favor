from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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

#calificacion
class Rating(models.Model):
    offer = models.ForeignKey('Ofertas', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    overall_experience = models.PositiveIntegerField(default=5)
    would_use_again = models.CharField(max_length=3)
    improvement_suggestions = models.TextField(blank=True, null=True)

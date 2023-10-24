from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

#ofertas
class Ofertas(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    datecompleted = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Ofertas"
    def __str__(self):
        return self.title + '- by ' + self.user.username

#calificacion
class Rating(models.Model):
    offer = models.ForeignKey('Ofertas', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('offer', 'user')


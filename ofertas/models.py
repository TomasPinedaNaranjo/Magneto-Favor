from django.db import models
from django.contrib.auth.models import User


class Ofertas(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    class Meta:
        verbose_name_plural = "Ofertas"
    def __str__(self):
        return self.title + '- by ' + self.user.username
   


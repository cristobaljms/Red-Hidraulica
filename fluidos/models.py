from django.db import models

# Create your models here.
class Fluido(models.Model):
    descripcion = models.CharField(max_length=80, default='')
    viscosidad_cinematica = models.CharField(max_length=30, default='') 
    valor_viscocidad = models.FloatField()
    
    def __str__(self):
        return '{}'.format(self.descripcion)
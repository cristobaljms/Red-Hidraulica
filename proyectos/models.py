from django.db import models

# Create your models here.

class Material(models.Model):
    descripcion = models.CharField(max_length=255, default='')
    ks = models.FloatField()

    def __str__(self):
        return '{}'.format(self.descripcion)

class Fluido(models.Model):
    descripcion = models.CharField(max_length=80, default='')
    viscosidad_cinematica    = models.CharField(max_length=30, default='') 
    valor_viscocidad = models.FloatField()
    
    def __str__(self):
        return '{}'.format(self.descripcion)
    
class Proyecto(models.Model):
    nombre =  models.CharField(max_length=100, default='')
    fluido = models.ForeignKey(Fluido, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
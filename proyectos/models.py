from django.db import models
from materiales.models import Material
from fluidos.models import Fluido
    
class Proyecto(models.Model):
    nombre =  models.CharField(max_length=100, default='')
    fluido = models.ForeignKey(Fluido, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.nombre)
        
class Nodo(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    numero = models.CharField(max_length=4, default='')
    demanda = models.FloatField()
    cota = models.FloatField()
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)

class Tuberia(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    numero = models.CharField(max_length=4, default='')
    longitud = models.FloatField()
    diametro = models.FloatField()
    km = models.FloatField(default=0)
    start = models.CharField(max_length=4, default='')
    end =  models.CharField(max_length=4, default='')


class Reservorio(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    numero = models.CharField(max_length=4, default='')
    z = models.FloatField()
    x_position = models.IntegerField(default=0)
    y_position = models.IntegerField(default=0)
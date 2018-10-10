from django.db import models
from materiales.models import Material
from fluidos.models import Fluido
    
class Proyecto(models.Model):
    nombre =  models.CharField(max_length=100, default='')
    fluido = models.ForeignKey(Fluido, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
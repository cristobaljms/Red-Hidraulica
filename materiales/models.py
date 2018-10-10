from django.db import models

# Create your models here.
class Material(models.Model):
    descripcion = models.CharField(max_length=255, default='')
    ks = models.FloatField()

    def __str__(self):
        return '{}'.format(self.descripcion)

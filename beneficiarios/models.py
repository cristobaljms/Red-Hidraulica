from django.db import models

# Create your models here.
"""
class Cargo(models.Model):
    nombre = models.CharField(max_length=255, default='')

    def __str__(self):
        return '{}'.format(self.nombre)

class Beneficiarios(models.Model):
    cedula = models.CharField(blank=False, max_length=12, primary_key=True)
    nombres = models.CharField(max_length=255, default='')
    cargo = models.CharField(max_length=255, default='')
    status = models.IntegerField(default=1)
"""    
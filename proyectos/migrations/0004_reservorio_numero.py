# Generated by Django 2.1.2 on 2018-10-13 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_reservorio'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservorio',
            name='numero',
            field=models.CharField(default='', max_length=4),
        ),
    ]
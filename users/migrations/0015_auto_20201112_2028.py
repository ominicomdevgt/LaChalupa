# Generated by Django 3.1.2 on 2020-11-13 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20201111_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='DNI',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Cedula'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-03 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20201028_1647'),
        ('game', '0009_auto_20201102_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='city',
        ),
        migrations.RemoveField(
            model_name='reward',
            name='country',
        ),
        migrations.RemoveField(
            model_name='reward',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='reward',
            name='longitude',
        ),
        migrations.AddField(
            model_name='reward',
            name='gender',
            field=models.CharField(max_length=100, null=True, verbose_name='Genero'),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('lat', models.FloatField(default=0, verbose_name='Latiud')),
                ('longitude', models.FloatField(default=0, verbose_name='Longitud')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.city', verbose_name='Municipio')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.country', verbose_name='Departamento')),
            ],
            options={
                'verbose_name': 'Tienda',
                'verbose_name_plural': 'Tiendas',
            },
        ),
    ]

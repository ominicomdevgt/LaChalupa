from django.db import models
from django.contrib.auth.models import User
from registration.models import Country,City
# Create your models here.
class Card(models.Model):
    description = models.CharField(max_length =100 , verbose_name="Descripción")
    image = models.ImageField(upload_to='game_pics', verbose_name="Imagen")
    sound = models.CharField(max_length=100, verbose_name='Audio', null=True)
    class Meta:
        verbose_name = "Carta"
        verbose_name_plural = "Cartas"

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    date = models.DateTimeField(verbose_name='Fecha del Juego')
    won = models.BooleanField(verbose_name='Ganado')
    reward = models.ForeignKey('Reward', related_name="rewards",on_delete=models.CASCADE, null=True , verbose_name='Premio')
    delivered = models.IntegerField(verbose_name='Entregado', default=0)
    cards = models.CharField(max_length=100,verbose_name='Carton', null=True)
    sing = models.CharField(max_length=100,verbose_name='Cantada', null=True)
    PID = models.IntegerField(default=0)
    store = models.ForeignKey('Store', on_delete=models.SET_NULL,verbose_name='Tienda', blank=True, null=True)
    date_reward = models.DateTimeField(verbose_name='Fecha Entrega premio', null=True)

class Reward(models.Model):
    Gender = (

        ('General', 'General'),
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),

    )
    types = (
        ('Camiseta', 'Camiseta'),
        ('Gorra', 'Gorra'),
        ('12 Pack Gratis', '12 Pack Gratis'),
        ('Juego de Mesa Chalupa', 'Juego de Mesa Chalupa'),
    )
    sizes = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('N/A', 'N/A'),
    )
    unit = models.IntegerField(verbose_name='Cantidad')
    size = models.CharField(max_length=255, verbose_name='Talla', choices=sizes, default='N/A')
    type_reward = models.CharField(max_length=255, verbose_name='Tipo', choices=types, null=True)
    image = models.ImageField(upload_to='game_pics', verbose_name="Imagen")    
    gender = models.CharField(max_length=100,choices = Gender ,null=True,verbose_name='Genero')
    #store = models.ForeignKey('Store', on_delete=models.SET_NULL,verbose_name='Tienda', blank=True, null=True)
    class Meta:
        verbose_name = "Premio"
        verbose_name_plural = "Premios"
    def __str__(self):
        return self.type_reward + '-'+ self.size + '-' +self.gender

class Reward_Verificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, verbose_name="Premio")
    location = models.CharField(max_length=255, verbose_name='Ubicacion')

class Store(models.Model):
    name = models.CharField(max_length=100,verbose_name='Nombre')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name='Departamento', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL,verbose_name='Municipio', blank=True, null=True)
    lat = models.FloatField(verbose_name='Latiud', default=0)
    longitude = models.FloatField(verbose_name='Longitud', default=0)
    group = models.IntegerField(verbose_name='Grupo',null=True)
    class Meta:
        verbose_name = "Tienda"
        verbose_name_plural = "Tiendas"
    def __str__(self):
        return self.name

class Stock(models.Model):
    unit = models.IntegerField(verbose_name='Cantidad')
    store = models.ForeignKey('Store', on_delete=models.CASCADE,verbose_name='Tienda')
    reward = models.ForeignKey('Reward', on_delete=models.CASCADE,verbose_name='Premio')
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventario"

class Conteo(models.Model):
    contador = models.IntegerField(verbose_name='Cantidad')
    reward = models.IntegerField(verbose_name='Premio', null=True)
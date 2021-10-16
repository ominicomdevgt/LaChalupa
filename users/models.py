from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from registration.models import Country, City
from game.models import Store
# Create your models here.

class Profile(models.Model):
    Gender = (
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    image = models.ImageField(upload_to='profile_pics', verbose_name="Imagen")
    birthday = models.DateField(null=True, verbose_name="Fecha Nacimiento")
    DNI = models.CharField(null=True,max_length =100, verbose_name='Cedula', unique=True)
    telephone = models.IntegerField(null=True, verbose_name="Celular")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, verbose_name='Departamento', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL,verbose_name='Municipio', blank=True, null=True)
    direction = models.CharField(max_length =100,blank=True, null=True, verbose_name="Dirección")
    verificate = models.BooleanField(default=False, verbose_name="Verificado")
    comment = models.CharField(max_length=1000,blank=True ,null=True,verbose_name="Commentario", default='Tu cuenta será verificada en breve.')
    count = models.IntegerField(default=4, verbose_name="Contador")
    gender = models.CharField(max_length=100,choices = Gender,verbose_name='Genero', null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL,verbose_name='Tienda asignada', blank=True, null=True)
    sendEmail = models.BooleanField(default=False, verbose_name="send")
    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
    
    

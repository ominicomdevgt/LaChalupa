from django.contrib import admin
from .models import Profile
from django.contrib.admin import ModelAdmin, register


@register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user','Nombres','Correo','telephone','verificate')

    def Correo(self,obj):
        return obj.user.email

    def Nombres(self,obj):
        return obj.user.first_name + ' ' + obj.user.last_name 
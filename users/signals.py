from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.template.loader import render_to_string
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        new_user = User.objects.filter(pk=instance.pk).first()
        new_user.email = new_user.username
        new_user.save()
        print('se guardo')

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


    
        
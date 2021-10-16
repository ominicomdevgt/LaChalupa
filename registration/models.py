from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length =100)
    content = models.TextField()
    date_posted = models.DateField(auto_now=True)
    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', related_name="cities",on_delete=models.CASCADE)
    def __str__(self):
        return self.name
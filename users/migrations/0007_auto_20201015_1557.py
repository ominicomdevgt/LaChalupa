# Generated by Django 3.1.2 on 2020-10-15 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201013_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='comment',
            field=models.CharField(max_length=255, null=True, verbose_name='Commentario'),
        ),
        migrations.AddField(
            model_name='profile',
            name='count',
            field=models.IntegerField(default=4, verbose_name='Contador'),
        ),
    ]

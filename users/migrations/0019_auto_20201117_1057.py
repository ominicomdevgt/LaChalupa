# Generated by Django 3.1.2 on 2020-11-17 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20201116_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='comment',
            field=models.CharField(blank=True, default='Tu cuenta será verificada en un periodo máximo de 12 horas', max_length=255, null=True, verbose_name='Commentario'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-17 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_game_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reward',
            name='type_reward',
            field=models.CharField(choices=[('Camiseta', 'Camiseta'), ('Gorra', 'Gorra'), ('12 Pack Gratis', '12 Pack Gratis'), ('Juego de Mesa Chalupa', 'Juego de Mesa Chalupa')], max_length=255, null=True, verbose_name='Tipo'),
        ),
    ]

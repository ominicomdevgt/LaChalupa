# Generated by Django 3.1.2 on 2020-10-29 16:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0005_auto_20201029_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='reward_verificate',
            name='reward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.reward', verbose_name='Premio'),
        ),
        migrations.AlterField(
            model_name='reward_verificate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]

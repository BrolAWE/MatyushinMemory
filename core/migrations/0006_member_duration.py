# Generated by Django 4.1.3 on 2022-12-02 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='duration',
            field=models.IntegerField(default=2000, verbose_name='Длительность в мс'),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-01 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_answer_was_shown_alter_answer_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docfile', models.FileField(blank=True, null=True, upload_to='update/%Y/%m/%d', verbose_name='Файл обновления')),
            ],
        ),
    ]

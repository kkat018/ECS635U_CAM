# Generated by Django 4.1.5 on 2023-05-01 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cam', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.IntegerField(blank=True, null=True, unique=True, verbose_name='Number'),
        ),
    ]

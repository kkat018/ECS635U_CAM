# Generated by Django 4.1.2 on 2023-04-21 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='location',
            field=models.TextField(default=None, max_length=50, null=True, verbose_name='location'),
        ),
    ]

# Generated by Django 4.2.14 on 2024-07-25 23:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customerprofile_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='phone_number',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number is not correct!', regex='^09[0-9]{9}$')], verbose_name='Phone Number'),
        ),
    ]

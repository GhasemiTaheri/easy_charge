# Generated by Django 4.2.14 on 2024-07-25 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorprofile',
            name='is_verify',
            field=models.BooleanField(default=True, verbose_name='Is Verified'),
        ),
    ]

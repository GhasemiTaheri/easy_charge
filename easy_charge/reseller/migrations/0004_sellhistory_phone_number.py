# Generated by Django 4.2.14 on 2024-07-26 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reseller', '0003_alter_creditrequest_vendor'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellhistory',
            name='phone_number',
            field=models.CharField(max_length=12, null=True, verbose_name='Phone number'),
        ),
    ]

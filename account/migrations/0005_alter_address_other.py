# Generated by Django 4.2.7 on 2024-04-18 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_shopuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='other',
            field=models.CharField(default=None, max_length=50),
        ),
    ]

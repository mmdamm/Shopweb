# Generated by Django 4.2.7 on 2024-04-18 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='account.address'),
        ),
    ]

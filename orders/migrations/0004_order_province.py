# Generated by Django 4.2.7 on 2024-07-14 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='province',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.7 on 2024-07-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('co', 'confirm'), ('qu', 'in queue'), ('re', 'received')], default='co', max_length=2),
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-15 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0008_trips_order_trips'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='cost',
            field=models.FloatField(default='0', max_length=10),
        ),
    ]
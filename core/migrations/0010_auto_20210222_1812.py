# Generated by Django 3.1.1 on 2021-02-22 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210221_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setitem',
            name='sushi_amount',
            field=models.FloatField(default=1, verbose_name='Количество'),
        ),
    ]

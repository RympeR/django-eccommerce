# Generated by Django 3.1.5 on 2021-01-27 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210127_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='label',
        ),
        migrations.AddField(
            model_name='category',
            name='label',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

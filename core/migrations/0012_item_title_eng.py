# Generated by Django 3.1.1 on 2021-02-01 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210201_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='title_eng',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
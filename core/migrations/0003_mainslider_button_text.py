# Generated by Django 3.1.1 on 2021-01-31 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_mainslider'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainslider',
            name='button_text',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Текст кнопки'),
        ),
    ]
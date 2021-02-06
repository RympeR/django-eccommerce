# Generated by Django 3.1.1 on 2021-02-01 17:07

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('propositions', '0003_auto_20210129_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='description_eng',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proposition',
            name='title_eng',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Заголовок eng'),
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_eng_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Название тэга'),
        ),
    ]
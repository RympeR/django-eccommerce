# Generated by Django 3.1.5 on 2021-01-29 09:00

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, verbose_name='Название тэга')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Proposition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='Заголовок')),
                ('date_added', models.DateField(auto_now=True)),
                ('proposition_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('description', tinymce.models.HTMLField()),
                ('tag', models.ManyToManyField(to='propositions.Tag')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
                'ordering': ['-date_added'],
            },
        ),
    ]

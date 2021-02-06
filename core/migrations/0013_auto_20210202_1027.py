# Generated by Django 3.1.1 on 2021-02-02 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_item_title_eng'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='label_eng',
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_percent',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
    ]
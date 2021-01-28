# Generated by Django 3.1.5 on 2021-01-28 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210127_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_type',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='default',
        ),
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ordered_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='shop.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='person_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(default=389999999999, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='sessinoOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.sessionorder'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='sessinoOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.sessionorder'),
        ),
        migrations.AddField(
            model_name='payment',
            name='sessinoOrder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.sessionorder'),
        ),
    ]

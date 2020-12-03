# Generated by Django 3.1.3 on 2020-12-03 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20201203_1024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleapply',
            name='items',
        ),
        migrations.AddField(
            model_name='saleapply',
            name='item',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.item'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-14 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20201112_1817'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['sale']},
        ),
        migrations.AddField(
            model_name='article',
            name='average_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='shop.brand'),
        ),
    ]
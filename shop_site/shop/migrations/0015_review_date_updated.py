# Generated by Django 3.1.2 on 2020-11-08 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20201108_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-07 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20201107_0843'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'name')},
        ),
    ]

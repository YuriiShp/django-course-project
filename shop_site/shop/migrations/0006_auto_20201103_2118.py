# Generated by Django 3.1.2 on 2020-11-03 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201101_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='main_title',
        ),
        migrations.RemoveField(
            model_name='category',
            name='pet',
        ),
        migrations.RemoveField(
            model_name='category',
            name='sub_title',
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='shop.category'),
        ),
        migrations.DeleteModel(
            name='MainTitle',
        ),
        migrations.DeleteModel(
            name='Pet',
        ),
        migrations.DeleteModel(
            name='SubTitle',
        ),
    ]

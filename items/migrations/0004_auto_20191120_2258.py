# Generated by Django 2.2.7 on 2019-11-20 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20191120_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(),
        ),
    ]

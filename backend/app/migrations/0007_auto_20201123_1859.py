# Generated by Django 3.1.3 on 2020-11-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20201121_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='minimal_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-04 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20201204_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileAvatar',
            field=models.ImageField(blank=True, default='../media/default.jpg', upload_to=''),
        ),
    ]
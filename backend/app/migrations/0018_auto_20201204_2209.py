# Generated by Django 3.0 on 2020-12-04 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20201204_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profileUserSurame',
            new_name='profileUserSurname',
        ),
    ]
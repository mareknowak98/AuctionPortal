# Generated by Django 3.1.4 on 2020-12-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20201204_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileBankAccountNr',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profileTelephoneNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

# Generated by Django 3.1.3 on 2020-11-29 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.OneToOneField(default=4, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='app.category'),
        ),
    ]
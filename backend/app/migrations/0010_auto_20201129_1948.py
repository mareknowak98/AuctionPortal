# Generated by Django 3.1.3 on 2020-11-29 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='app.category'),
        ),
    ]

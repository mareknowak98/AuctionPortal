# Generated by Django 3.1.3 on 2020-11-21 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_highest_bid', models.IntegerField()),
                ('date_started', models.DateTimeField()),
                ('date_end', models.DateTimeField()),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('highest_bid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('minimal_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('is_shipping_av', models.BooleanField()),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='app.product')),
                ('user_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

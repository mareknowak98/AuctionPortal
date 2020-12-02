# Generated by Django 3.1.3 on 2020-12-02 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_auction_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bidPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bidDate', models.DateTimeField(auto_now_add=True)),
                ('bidAuction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.auction')),
                ('bidUserBuyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
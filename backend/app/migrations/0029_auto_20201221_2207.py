# Generated by Django 3.1.4 on 2020-12-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auction_auctionshippingcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.ImageField(blank=True, default='../media/default_auction.jpg', null=True, upload_to='images/'),
        ),
    ]

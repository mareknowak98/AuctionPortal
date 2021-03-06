# Generated by Django 3.1.4 on 2020-12-08 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0023_auto_20201205_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useropinion',
            name='opinionUserAbout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAbout', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='useropinion',
            name='opinionUserAuthor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAuthor', to=settings.AUTH_USER_MODEL),
        ),
    ]

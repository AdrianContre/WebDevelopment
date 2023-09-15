# Generated by Django 4.2.2 on 2023-07-10 16:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctionlisting_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='passengers', to=settings.AUTH_USER_MODEL),
        ),
    ]
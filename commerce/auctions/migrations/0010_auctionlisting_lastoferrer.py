# Generated by Django 4.2.2 on 2023-07-13 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='lastOferrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lastOferrer', to=settings.AUTH_USER_MODEL),
        ),
    ]

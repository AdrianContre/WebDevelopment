# Generated by Django 4.2.2 on 2023-07-15 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_bid_unique_together_bid_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='postList', to='auctions.auctionlisting')),
                ('poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
                'unique_together': {('poster', 'list', 'created_on')},
            },
        ),
    ]

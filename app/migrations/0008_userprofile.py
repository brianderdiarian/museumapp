# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-18 18:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_auto_20170410_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_artist', models.ManyToManyField(null=True, to='app.Artist')),
                ('queued_artworks', models.ManyToManyField(null=True, related_name='queued', to='app.Artwork')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('viewed_artworks', models.ManyToManyField(null=True, related_name='viewed', to='app.Artwork')),
            ],
        ),
    ]
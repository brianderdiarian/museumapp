# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 00:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_artist_collection_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='display',
            name='artwork',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Artwork'),
        ),
        migrations.AddField(
            model_name='display',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Collection'),
        ),
    ]
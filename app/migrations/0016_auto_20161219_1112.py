# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-19 19:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_artwork_movements'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='artist_sans_accents',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='collection_address',
        ),
    ]
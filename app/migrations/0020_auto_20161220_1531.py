# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-20 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20161220_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artist_sans_accents',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-19 17:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_artwork_died'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='descriptors',
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='nationality',
        ),
    ]

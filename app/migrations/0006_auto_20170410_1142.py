# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-10 18:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170409_2018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['artist']},
        ),
    ]
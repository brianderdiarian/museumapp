# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-19 03:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20170103_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
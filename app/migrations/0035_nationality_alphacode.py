# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 04:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='nationality',
            name='alphacode',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
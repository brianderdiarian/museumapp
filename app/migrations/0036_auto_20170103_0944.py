# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-03 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_nationality_alphacode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nationality',
            name='alphacode',
        ),
        migrations.AddField(
            model_name='nationality',
            name='nation',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

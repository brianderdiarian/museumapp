# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-22 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20170218_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastCrawl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spider_name', models.CharField(max_length=255)),
                ('last_crawled', models.DateField(null=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-13 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('artist_sans_accents', models.CharField(blank=True, max_length=255)),
                ('movements', models.CharField(blank=True, max_length=255)),
                ('sex', models.CharField(blank=True, max_length=255)),
                ('born', models.CharField(blank=True, max_length=255)),
                ('died', models.CharField(blank=True, max_length=255)),
                ('descriptors', models.CharField(blank=True, max_length=255)),
                ('nationality', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('artist_sans_accents', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('title_sans_accents', models.CharField(blank=True, max_length=255)),
                ('date', models.CharField(blank=True, max_length=255)),
                ('medium', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('dimensions', models.CharField(max_length=255)),
                ('coordinates', models.CharField(max_length=255)),
                ('pageurl', models.CharField(max_length=255)),
                ('accession_number', models.CharField(blank=True, max_length=255)),
                ('imageurl', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateField(null=True)),
                ('sex', models.CharField(blank=True, max_length=255)),
                ('born', models.CharField(blank=True, max_length=255)),
                ('died', models.CharField(blank=True, max_length=255)),
                ('collection', models.CharField(blank=True, max_length=255)),
                ('movements', models.CharField(blank=True, max_length=255)),
                ('descriptors', models.CharField(blank=True, max_length=255)),
                ('nationality', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_name', models.CharField(blank=True, max_length=255)),
                ('collection_address', models.CharField(blank=True, max_length=255)),
                ('coordinates', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('meta', models.TextField(blank=True)),
            ],
        ),
    ]

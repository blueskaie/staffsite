# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffapp', '0004_requestjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestjob',
            name='processed',
            field=models.BooleanField(default=0),
        ),
    ]
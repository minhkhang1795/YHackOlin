# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0010_auto_20171202_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='experiences',
            field=models.ManyToManyField(blank=True, null=True, to='social_app.Experience'),
        ),
    ]

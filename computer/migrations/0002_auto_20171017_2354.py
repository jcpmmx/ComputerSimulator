# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-17 23:54
from __future__ import unicode_literals

import computer.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='id',
            field=models.CharField(default=computer.utils.generate_computer_id, editable=False, max_length=7, primary_key=True, serialize=False),
        ),
    ]

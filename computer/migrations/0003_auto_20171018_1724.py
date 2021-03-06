# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-18 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('computer', '0002_auto_20171017_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='program_stack_pointer',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='computer',
            name='program_stack_size',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='computer',
            name='program_stack',
            field=jsonfield.fields.JSONField(default={}, verbose_name='Data of the program stack'),
        ),
        migrations.DeleteModel(
            name='ProgramStack',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20150607_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fishingevent',
            name='event_type',
            field=models.CharField(max_length=64, choices=[('catch', 'Catch'), ('poacher', 'Poaching Incident'), ('accident', 'Accident')], help_text='What type of event was reported.'),
        ),
    ]

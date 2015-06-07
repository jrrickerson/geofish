# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20150607_0252'),
    ]

    operations = [
        migrations.CreateModel(
            name='FishingEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('device', models.CharField(max_length=512, help_text='Unique id of the device reporting this event.')),
                ('latitude', models.FloatField(null=True, help_text='Latitude of this event location.', blank=True)),
                ('longitude', models.FloatField(null=True, help_text='Longitude of this event location.', blank=True)),
                ('timestamp', models.DateTimeField(help_text='Date and time when the event occurred.')),
                ('event_type', models.CharField(max_length=64, help_text='What type of event was reported.')),
                ('size', models.CharField(help_text='Approximate size of the animal related to this event.', max_length=128, blank=True)),
                ('weight', models.CharField(help_text='Approximate weight of the animal related to this event.', max_length=128, blank=True)),
                ('notes', models.TextField(help_text='Additional notes or information about this incident', blank=True)),
                ('region', models.ForeignKey(to='data.Region', help_text='Region where this event occurred.')),
                ('species', models.ForeignKey(blank=True, help_text='Species of the animal related to this event, if known.', null=True, to='data.Species')),
            ],
        ),
        migrations.AddField(
            model_name='regionspecies',
            name='season_end',
            field=models.DateField(null=True, help_text='End of fishing season for this species in this region', blank=True),
        ),
        migrations.AddField(
            model_name='regionspecies',
            name='season_start',
            field=models.DateField(null=True, help_text='Start of fishing season for this species in this region', blank=True),
        ),
    ]

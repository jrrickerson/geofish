# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='regionspecies',
            name='size_limit_qualifier',
            field=models.CharField(max_length=512, blank=True, help_text='Qualifier for the size limit (unit, per day, per season, etc.)'),
        ),
        migrations.AlterField(
            model_name='region',
            name='limits',
            field=models.ManyToManyField(related_name='regions', blank=True, to='data.Limit', help_text='General fishing limits applied to this region.'),
        ),
        migrations.AlterField(
            model_name='region',
            name='regulations',
            field=models.ManyToManyField(related_name='regions', blank=True, to='data.Regulation', help_text='Legal regulations which apply to this region.'),
        ),
        migrations.AlterField(
            model_name='region',
            name='unlawful_actions',
            field=models.ManyToManyField(related_name='regions', blank=True, to='data.UnlawfulAction', help_text='Unlawful actions which apply to this region.'),
        ),
        migrations.AlterField(
            model_name='regionspecies',
            name='catch_limit_qualifier',
            field=models.CharField(max_length=512, blank=True, help_text='Qualifier for the catch limit (unit, per day, per season, etc.)'),
        ),
    ]

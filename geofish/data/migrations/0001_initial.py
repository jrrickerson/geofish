# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Limit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('amount', models.FloatField(help_text='Amount of fish, pounds, etc. which constitutes the limit.')),
                ('amount_qualifier', models.CharField(max_length=512, help_text='Qualifier for the amount (unit, per day, per season, etc.)')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=1024, help_text='Name of this region.')),
                ('limits', models.ManyToManyField(related_name='regions', help_text='General fishing limits applied to this region.', to='data.Limit')),
                ('parent_region', models.ForeignKey(related_name='child_regions', to='data.Region', null=True, blank=True, help_text='Another region which contains or controls this region from a regulation standpoint.')),
            ],
        ),
        migrations.CreateModel(
            name='RegionSpecies',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('catch_limit', models.PositiveIntegerField(blank=True, null=True, help_text='Catch limit for this species in this region.')),
                ('size_limit', models.FloatField(blank=True, null=True, help_text='Size limit for this species in this region.')),
                ('catch_limit_qualifier', models.CharField(max_length=512, help_text='Qualifier for the size limit (unit, per day, per season, etc.)')),
                ('best_bet', models.BooleanField(default=False, help_text='This species is a "best bet" catch for this region.')),
                ('record_size', models.CharField(blank=True, max_length=1024, help_text='The record size catch of this species in this region')),
                ('region', models.ForeignKey(to='data.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('regulation_id', models.CharField(max_length=1024, help_text='Legal identifier or lookup name for this regulation.')),
                ('full_regulation_text', models.TextField(help_text='Full legal text of this regulation.')),
            ],
        ),
        migrations.CreateModel(
            name='RegulatoryBody',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=1024, help_text='Name of the regulatory body which has jurisdiction over this fishing region.')),
                ('email', models.EmailField(blank=True, max_length=254, help_text='Email address to use to contact this regulatory body.')),
                ('phone', models.CharField(max_length=128, help_text='Phone number to use to contact to contact this regulatory body.')),
                ('website', models.CharField(max_length=1024, help_text='Website to use to find more info from this regulatory body.')),
                ('additional_info', models.TextField(blank=True, help_text='Additional information (hours, contact names, other instructions.')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('common_name', models.CharField(blank=True, max_length=1024, help_text='Common or ordinary name for this species.')),
                ('scientific_name', models.CharField(max_length=1024, help_text='Scientific name for this species.')),
                ('regions', models.ManyToManyField(related_name='species', through='data.RegionSpecies', help_text='Regions where this species can be found.', to='data.Region')),
            ],
        ),
        migrations.CreateModel(
            name='UnlawfulAction',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('action_text', models.CharField(max_length=1024, help_text='Simple text explanation of the unlawful action which applies to this time or location.')),
                ('time_constraint_start', models.TimeField(blank=True, null=True, help_text='Start time of this unlawful action, if applicable.')),
                ('time_constraint_end', models.TimeField(blank=True, null=True, help_text='End time of this unlawful action, if applicable.')),
                ('date_constraint_start', models.TimeField(blank=True, null=True, help_text='Start date of this unlawful action, if applicable.')),
                ('date_constraint_end', models.TimeField(blank=True, null=True, help_text='End date of this unlawful action, if applicable.')),
                ('exclusions', models.ManyToManyField(blank=True, help_text='Child regions which are specific exclusions for this unlawful action.', to='data.Region')),
            ],
        ),
        migrations.AddField(
            model_name='regionspecies',
            name='species',
            field=models.ForeignKey(to='data.Species'),
        ),
        migrations.AddField(
            model_name='region',
            name='regulations',
            field=models.ManyToManyField(related_name='regions', help_text='Legal regulations which apply to this region.', to='data.Regulation'),
        ),
        migrations.AddField(
            model_name='region',
            name='regulatory_body',
            field=models.ForeignKey(related_name='regions', blank=True, help_text='Regulatory body / organiztion which has jurisdiction in this region.', to='data.RegulatoryBody'),
        ),
        migrations.AddField(
            model_name='region',
            name='unlawful_actions',
            field=models.ManyToManyField(related_name='regions', help_text='Unlawful actions which apply to this region.', to='data.UnlawfulAction'),
        ),
    ]

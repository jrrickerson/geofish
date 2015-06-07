from django.db import models
#from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

#
# Regulation and informational data models
# NOTE: Each of these should be tied to a particular geofenced region
#

class Region(models.Model):
    name = models.CharField(max_length=1024,
        help_text=_('Name of this region.'))
    parent_region = models.ForeignKey('self', blank=True, null=True, related_name='child_regions',
        help_text=_('Another region which contains or controls this region from a regulation standpoint.'))

    regulatory_body = models.ForeignKey('RegulatoryBody', blank=True, related_name='regions',
        help_text=_('Regulatory body / organiztion which has jurisdiction in this region.'))

    #mpoly = models.MultiPolygonField(
    #    help_text=_('Geographical areas / shapes which define this region.'))
    #objects = models.GeoManager()

    limits = models.ManyToManyField('Limit', related_name='regions',
        help_text=_('General fishing limits applied to this region.'))
    regulations = models.ManyToManyField('Regulation', related_name='regions',
        help_text=_('Legal regulations which apply to this region.'))
    unlawful_actions = models.ManyToManyField('UnlawfulAction', related_name='regions',
        help_text=_('Unlawful actions which apply to this region.'))


class RegulatoryBody(models.Model):
    name = models.CharField(max_length=1024,
        help_text=_('Name of the regulatory body which has jurisdiction over this fishing region.'))
    email = models.EmailField(blank=True,
        help_text=_('Email address to use to contact this regulatory body.'))
    phone = models.CharField(max_length=128,
        help_text=_('Phone number to use to contact to contact this regulatory body.'))
    website = models.CharField(max_length=1024,
        help_text=_('Website to use to find more info from this regulatory body.'))
    additional_info = models.TextField(blank=True,
        help_text=_('Additional information (hours, contact names, other instructions.'))


class Regulation(models.Model):
    regulation_id = models.CharField(max_length=1024,
        help_text=_('Legal identifier or lookup name for this regulation.'))
    full_regulation_text = models.TextField(
        help_text=_('Full legal text of this regulation.'))


class Limit(models.Model):
    amount = models.FloatField(
        help_text=_('Amount of fish, pounds, etc. which constitutes the limit.'))
    amount_qualifier = models.CharField(max_length=512,
        help_text=_('Qualifier for the amount (unit, per day, per season, etc.)'))


class UnlawfulAction(models.Model):
    action_text = models.CharField(max_length=1024,
        help_text=_('Simple text explanation of the unlawful action which applies to this time or location.'))
    time_constraint_start = models.TimeField(blank=True, null=True,
        help_text=_('Start time of this unlawful action, if applicable.'))
    time_constraint_end = models.TimeField(blank=True, null=True,
        help_text=_('End time of this unlawful action, if applicable.'))
    date_constraint_start = models.TimeField(blank=True, null=True,
        help_text=_('Start date of this unlawful action, if applicable.'))
    date_constraint_end = models.TimeField(blank=True, null=True,
        help_text=_('End date of this unlawful action, if applicable.'))
    exclusions = models.ManyToManyField(Region, blank=True,
        help_text=_('Child regions which are specific exclusions for this unlawful action.'))


class Species(models.Model):
    common_name = models.CharField(max_length=1024, blank=True,
        help_text=_('Common or ordinary name for this species.'))
    scientific_name = models.CharField(max_length=1024,
        help_text=_('Scientific name for this species.'))

    regions = models.ManyToManyField(Region, through='RegionSpecies', related_name='species',
        help_text=_('Regions where this species can be found.'))


class RegionSpecies(models.Model):
    """ Specific information about this species pertaining to this particular region. """
    region = models.ForeignKey(Region)
    species = models.ForeignKey(Species)

    catch_limit = models.PositiveIntegerField(blank=True, null=True,
        help_text=_('Catch limit for this species in this region.'))
    catch_limit_qualifier = models.CharField(max_length=512,
        help_text=_('Qualifier for the catch limit (unit, per day, per season, etc.)'))
    size_limit = models.FloatField(blank=True, null=True,
        help_text=_('Size limit for this species in this region.'))
    catch_limit_qualifier = models.CharField(max_length=512,
        help_text=_('Qualifier for the size limit (unit, per day, per season, etc.)'))

    best_bet = models.BooleanField(default=False,
        help_text=_('This species is a "best bet" catch for this region.'))
    record_size = models.CharField(max_length=1024, blank=True,
        help_text=_('The record size catch of this species in this region'))



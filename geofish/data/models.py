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

    limits = models.ManyToManyField('Limit', related_name='regions', blank=True,
        help_text=_('General fishing limits applied to this region.'))
    regulations = models.ManyToManyField('Regulation', related_name='regions', blank=True,
        help_text=_('Legal regulations which apply to this region.'))
    unlawful_actions = models.ManyToManyField('UnlawfulAction', related_name='regions', blank=True,
        help_text=_('Unlawful actions which apply to this region.'))

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name


class Regulation(models.Model):
    regulation_id = models.CharField(max_length=1024,
        help_text=_('Legal identifier or lookup name for this regulation.'))
    full_regulation_text = models.TextField(
        help_text=_('Full legal text of this regulation.'))

    def __str__(self):
        return self.regulation_id


class Limit(models.Model):
    amount = models.FloatField(
        help_text=_('Amount of fish, pounds, etc. which constitutes the limit.'))
    amount_qualifier = models.CharField(max_length=512,
        help_text=_('Qualifier for the amount (unit, per day, per season, etc.)'))

    def __str__(self):
        return '{} {}'.format(self.amount, self.amount_qualifier)


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

    def __str__(self):
        return self.action_text if len(self.action_text) < 40 else '{}...'.format(self.action_text[:37])


class Species(models.Model):
    common_name = models.CharField(max_length=1024, blank=True,
        help_text=_('Common or ordinary name for this species.'))
    scientific_name = models.CharField(max_length=1024,
        help_text=_('Scientific name for this species.'))

    regions = models.ManyToManyField(Region, through='RegionSpecies', related_name='species',
        help_text=_('Regions where this species can be found.'))

    def __str__(self):
        return self.common_name if self.common_name else self.scientific_name


class RegionSpecies(models.Model):
    """ Specific information about this species pertaining to this particular region. """
    region = models.ForeignKey(Region)
    species = models.ForeignKey(Species)

    catch_limit = models.PositiveIntegerField(blank=True, null=True,
        help_text=_('Catch limit for this species in this region.'))
    catch_limit_qualifier = models.CharField(max_length=512, blank=True,
        help_text=_('Qualifier for the catch limit (unit, per day, per season, etc.)'))
    size_limit = models.FloatField(blank=True, null=True,
        help_text=_('Size limit for this species in this region.'))
    size_limit_qualifier = models.CharField(max_length=512, blank=True,
        help_text=_('Qualifier for the size limit (unit, per day, per season, etc.)'))
    season_start = models.DateField(blank=True, null=True,
        help_text=_('Start of fishing season for this species in this region'))
    season_end = models.DateField(blank=True, null=True,
        help_text=_('End of fishing season for this species in this region'))

    best_bet = models.BooleanField(default=False,
        help_text=_('This species is a "best bet" catch for this region.'))
    record_size = models.CharField(max_length=1024, blank=True,
        help_text=_('The record size catch of this species in this region'))

    def __str__(self):
        return '{} [{}]'.format(str(self.species), self.region.name)


class FishingEvent(models.Model):
    CATCH = 'catch'
    POACHER = 'poacher'
    ACCIDENT = 'accident'
    TYPE_CHOICES = (
        (CATCH, 'Catch'),
        (POACHER, 'Poaching Incident'),
        (ACCIDENT, 'Accident'),
    )

    device = models.CharField(max_length=512,
        help_text=_('Unique id of the device reporting this event.'))
    latitude = models.FloatField(blank=True, null=True,
        help_text=_('Latitude of this event location.'))
    longitude = models.FloatField(blank=True, null=True,
        help_text=_('Longitude of this event location.'))
    region = models.ForeignKey(Region,
        help_text=_('Region where this event occurred.'))
    timestamp = models.DateTimeField(
        help_text=_('Date and time when the event occurred.'))
    event_type = models.CharField(max_length=64, choices=TYPE_CHOICES,
        help_text=_('What type of event was reported.'))
    species = models.ForeignKey(Species, blank=True, null=True,
        help_text=_('Species of the animal related to this event, if known.'))
    size = models.CharField(max_length=128, blank=True,
        help_text=_('Approximate size of the animal related to this event.'))
    weight = models.CharField(max_length=128, blank=True,
        help_text=_('Approximate weight of the animal related to this event.'))
    notes = models.TextField(blank=True,
        help_text=_('Additional notes or information about this incident'))

    def __str__(self):
        types = dict(self.TYPE_CHOICES)
        return '{} [{}, {}] at {}'.format(types[self.event_type], self.device, self.region, self.timestamp)

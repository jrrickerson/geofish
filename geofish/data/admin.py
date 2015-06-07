from django.contrib import admin

from .models import (Region, RegulatoryBody, Regulation, Limit, UnlawfulAction,
    Species, RegionSpecies, FishingEvent) 


class RegionSpeciesInline(admin.StackedInline):
    model = RegionSpecies
    extra = 0
    verbose_name = 'Species'
    verbose_name_plural = 'Species for Region'


class RegionAdmin(admin.ModelAdmin):
    inlines = [RegionSpeciesInline]


admin.site.register(Region, RegionAdmin)
admin.site.register(RegulatoryBody)
admin.site.register(Regulation)
admin.site.register(Limit)
admin.site.register(UnlawfulAction)
admin.site.register(Species)
admin.site.register(FishingEvent)

from django.contrib import admin

from .models import (Region, RegulatoryBody, Regulation, Limit, UnlawfulAction,
    Species,) 


admin.site.register(Region)
admin.site.register(RegulatoryBody)
admin.site.register(Regulation)
admin.site.register(Limit)
admin.site.register(UnlawfulAction)
admin.site.register(Species)

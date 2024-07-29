from django.contrib import admin

# Register your models here.

from .models import (ExcursionOrganizer, Excursion, Location, ExcursionLocation)

admin.site.register(ExcursionOrganizer)
admin.site.register(Excursion)
admin.site.register(Location)
admin.site.register(ExcursionLocation)
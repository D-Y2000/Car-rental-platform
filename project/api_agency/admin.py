from django.contrib import admin
from api_agency import models 

admin.site.register(models.User)
admin.site.register(models.Agency)
admin.site.register(models.Branch)
admin.site.register(models.Make)
admin.site.register(models.Model)
admin.site.register(models.Vehicle)
admin.site.register(models.Wilaya)
admin.site.register(models.Reservation)
admin.site.register(models.Notification)
admin.site.register(models.Rate)
admin.site.register(models.Feedback)
admin.site.register(models.Plan)
admin.site.register(models.Subscription)
admin.site.register(models.VehicleImage)
admin.site.register(models.LocationImage)
admin.site.register(models.NewSubscription)

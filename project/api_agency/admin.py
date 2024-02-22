from django.contrib import admin
from api_agency.models import * 
# Register your models here.

admin.site.register(User)
admin.site.register(Agency)
admin.site.register(Branch)
admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Vehicle)

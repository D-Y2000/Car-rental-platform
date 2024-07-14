from django.contrib import admin
from api_activity.models import *
# Register your models here.

admin.site.register(Activity)
admin.site.register(ActivityCategory)
admin.site.register(ActivityRate)
admin.site.register(ActivityFeedback)
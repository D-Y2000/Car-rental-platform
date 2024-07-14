from django.db.models.signals import post_save
from django.dispatch import receiver
from api_activity.models import ActivityRate
from django.db.models import Avg

@receiver(signal=post_save,sender=ActivityRate)
def calculate_destination_rate(sender,instance,created,**kwargs):
# Get the average rating for the destination
    activity = instance.activity
    rates=ActivityRate.objects.filter(activity=activity)
    average_rating = ActivityRate.objects.filter(activity=activity).aggregate(Avg('rate'))['rate__avg']
    # Update the overall rating of the activity
    activity.rate = average_rating
    activity.save()
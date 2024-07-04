from django.db.models.signals import post_save
from django.dispatch import receiver
from api_destination.models import Rate
from django.db.models import Avg

@receiver(signal=post_save,sender=Rate)
def calculate_destination_rate(sender,instance,created,**kwargs):
# Get the average rating for the destination
    destination = instance.destination
    rates=Rate.objects.filter(destination=destination)
    average_rating = Rate.objects.filter(destination=destination).aggregate(Avg('rate'))['rate__avg']
    # Update the overall rating of the destination
    destination.rate = average_rating
    destination.save()
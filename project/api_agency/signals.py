from django.db.models.signals import post_save
from django.dispatch import receiver
from api_agency.models import Notification,Reservation,Rate
from django.db.models import Avg

@receiver(signal=post_save,sender=Reservation)
def OrderNotification(sender,instance,created,**kwargs):
    if created : 
        user = instance.branch.agency.user
        message = 'A new order is made'
        reservation = instance
        
    else :
        user = instance.client.user
        message = 'Your order has been processed.'
        reservation = instance
    notification = Notification.objects.create(user=user,message=message,reservation = reservation)


@receiver(signal=post_save,sender=Rate)
def calculate_agency_rate(sender,instance,created,**kwargs):
# Get the average rating for the agency
    agency = instance.agency
    rates=Rate.objects.filter(agency=agency)
    average_rating = Rate.objects.filter(agency=agency).aggregate(Avg('rate'))['rate__avg']
    # Update the overall rating of the agency
    agency.rate = average_rating
    agency.save()
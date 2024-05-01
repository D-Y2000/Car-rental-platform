from django.db.models.signals import post_save
from django.dispatch import receiver
from api_agency.models import Notification,Reservation


@receiver(signal=post_save,sender=Reservation)
def OrderNotification(sender,instance,created,**kwargs):
    if created : 
        user = instance.agency.user
        message = 'A new order is made'
        reservation = instance
        
    else :
        user = instance.client.user
        message = 'Your order has been processed.'
        reservation = instance
    notification = Notification.objects.create(user=user,message=message,reservation = reservation)


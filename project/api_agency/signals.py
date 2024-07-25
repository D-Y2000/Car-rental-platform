from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from api_agency.models import Notification,Reservation,Rate,Subscription,Plan,Branch,Vehicle,Agency,NewSubscription
from django.db.models import Avg
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string


@receiver(signal=post_save,sender=Reservation)
def OrderNotification(sender,instance,created,**kwargs):
    if created : 
        # Send an email to the agency (vehicle owner)
        user = instance.branch.agency.user
        message = 'A new order is made'
        reservation = instance

        subject = 'Reservation - New Order'
        html_content = render_to_string("emails/new_order.html", {
            'user': 'user',
            'reservation': reservation
        })
        email = EmailMessage(
            subject = subject,
            body = html_content,
            to=[user.email]
        )

        email.content_subtype = "html"
        email.send()
        
    elif instance.status != 'postponed' :
        # Send an email to the client
        user = instance.client.user
        message = 'Your order has been processed.'
        reservation = instance

        subject = 'Reservation - Order Processed'
        html_content = render_to_string("emails/order_processed.html", {
            'user': 'user',
            'reservation': reservation
        })
        email = EmailMessage(
            subject = subject,
            body = html_content,
            to=[user.email]
        )

        email.content_subtype = "html"
        email.send()

    Notification.objects.create(user = user, message = message, reservation = reservation)
    

@receiver(signal=post_save,sender=Rate)
def calculate_agency_rate(sender,instance,created,**kwargs):
# Get the average rating for the agency
    agency = instance.agency
    rates=Rate.objects.filter(agency=agency)
    average_rating = Rate.objects.filter(agency=agency).aggregate(Avg('rate'))['rate__avg']
    # Update the overall rating of the agency
    agency.rate = average_rating
    agency.save()


@receiver(signal=post_save,sender=NewSubscription)
def subscribe_agency(sender,instance,created,**kwargs):
    subscription = instance
    if  created:
        agency=instance.agency
        agency_branches = Branch.objects.filter(agency=agency)
        free_plan = Plan.objects.get(name='free')
        if agency_branches.count() > free_plan.max_branches:
            branches_to_unlock = agency_branches[free_plan.max_branches:]
            print("unlocking branches")
            for branch in branches_to_unlock:
                branch_vehicles = Vehicle.objects.filter(owned_by = branch)
                print("unlocking vehicles")
                for vehicle in branch_vehicles:
                    vehicle.is_locked = False
                    vehicle.is_available = True
                    vehicle.save()
                branch.is_locked = False
                print("unlocked branch")
                branch.save()
        unlocked_agency_branches=agency_branches[:free_plan.max_branches]
        for branch in unlocked_agency_branches:
            branch_vehicles = Vehicle.objects.filter(owned_by = branch)
            if branch_vehicles.count() > free_plan.max_vehicles:
                branch_vehicles_to_lock = branch_vehicles[free_plan.max_vehicles:]
                print("unlocking unlocked branch  vehicles")
                for vehicle in branch_vehicles_to_lock:
                    vehicle.is_locked = False
                    vehicle.is_available = True
                    vehicle.save()



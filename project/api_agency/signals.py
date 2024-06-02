from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from api_agency.models import Notification,Reservation,Rate,Subscription,Plan,Branch,Vehicle,Agency
from django.db.models import Avg
from django.utils import timezone

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

unsubscribe = Signal()

@receiver(signal=unsubscribe,sender=Subscription)
def unsubscribe_agency(sender,instance,created,**kwargs):
    if not created and instance.end_at < timezone.now():
        print(f" starting unsebscription")
        agency = instance.agency
        agency_branches = Branch.objects.filter(agency=agency)
        free_plan = Plan.objects.get(name='free')
        unlocked_agency_branches=Branch.objects.filter(agency=agency)[:free_plan.max_branches]
        print(free_plan)
        if agency_branches.count() >= free_plan.max_branches:
            branches_to_lock = Branch.objects.filter(agency=agency)[free_plan.max_branches:]
            #lock all branches and vehicles relaetd to the branches to lock
            print("locking branches")
            for branch in branches_to_lock:
                branch_vehicles = Vehicle.objects.filter(owned_by = branch)
                print("locking branch  vehicles")
                for vehicle in branch_vehicles:
                    vehicle.is_locked = True
                    vehicle.is_available = False
                    vehicle.save()
                print("locking branch")
                branch.is_locked = True
                branch.save()
        #lock vehicles of unlocked branches
        print("unlocked branches")
        for branch in unlocked_agency_branches:
            branch_vehicles = Vehicle.objects.filter(owned_by = branch)
            if branch_vehicles.count() > free_plan.max_vehicles:
                branch_vehicles_to_lock = branch_vehicles[free_plan.max_vehicles:]
                print("locking unlocked branch  vehicles")
                for vehicle in branch_vehicles_to_lock:
                    vehicle.is_locked = True
                    vehicle.is_available = False
                    vehicle.save()
            branch.is_locked = True
            branch.save()


@receiver(signal=post_save,sender=Subscription)
def subscribe_agency(sender,instance,created,**kwargs):
    subscription = instance
    if  created:
        agency=instance.agency
        agency_branches = Branch.objects.filter(agency=agency)
        free_plan = Plan.objects.get(name='free')
        if agency_branches.count() >= free_plan.max_branches:
            branches_to_unlock = Branch.objects.filter(agency=agency)[free_plan.max_branches:]
            for branch in branches_to_unlock:
                branch_vehicles = Vehicle.objects.filter(owned_by = branch)
                if branch_vehicles.count() >= free_plan.max_vehicles:
                    branch_vehicles = branch_vehicles[free_plan.max_vehicles:]
                    for vehicle in branch_vehicles:
                        vehicle.is_locked = False
                        vehicle.is_available = True
                        vehicle.save()
                branch.is_locked = False
                branch.save()
    



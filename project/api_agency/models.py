from datetime import datetime,timedelta
from django.db import models
from api_main.models import Profile
from api_auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from dateutil.relativedelta import relativedelta


# Subscription Plan
# Free or Pro
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)


    # *** Limits ***
    # IF unlimited is True, then max value (limitation) is ignored
    unlimited_vehicles = models.BooleanField(default=False)
    unlimited_branches = models.BooleanField(default=False)

    # Limitation only for not unlimited (ignored whene unlimited is True)
    max_branches = models.PositiveSmallIntegerField(default=1)
    max_vehicles = models.PositiveSmallIntegerField(default=1)
    

    def __str__(self) -> str:
        return self.name

class NewSubscription(models.Model):
    # link to the payment checkout
    checkout_id = models.CharField(max_length=255, unique=True)
    # status: pending, paid, failed
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES ,default='pending')
    # plan: Free or Pro
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    # User who subscribed
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE, related_name='my_new_subscriptions')
    # *** Dates ***
    created_at = models.DateTimeField(auto_now_add=True)    
    # Note: end_at initialized for one month after created_at
    end_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.end_at:
            # Set end_at to one month after created_at
            self.end_at = datetime.now() + relativedelta(months=1)
        super().save(*args, **kwargs)

class Subscription(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    agency = models.ForeignKey('Agency', on_delete=models.CASCADE, related_name='my_subscriptions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Note: end_at initialized for one month after created_at
    end_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.end_at:
            # Set end_at to one month after created_at
            self.end_at = datetime.now() + relativedelta(months=1)
        super().save(*args, **kwargs)


# the agency model just a profile of agency that can ber rolled by agency owner which is just a user with role agency_owner 
# the agency need to be validate by the admin (Platform Owner) to be able to use the system
class Agency(models.Model):
    # User represents the admin of the agency or the owner who created the agency [One Admin]
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='my_agency')
    is_validated = models.BooleanField(default=False)

    name = models.CharField(max_length=150, null=False, blank=False)
    bio = models.TextField(blank=True)
    
    # contact info
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    rate  = models.FloatField(default=0,)


    license_doc = models.ImageField(null=True,blank=True)
    photo = models.ImageField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Rate(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE,related_name="my_ratings")
    rate  = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=1.0)

class Wilaya(models.Model):
    code = models.IntegerField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    ar_name = models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)

    clicks_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering=['code']
    
    def __str__(self) -> str:
        return self.name

class LocationImage(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='images')
    url = models.URLField(default=('https://placehold.co/600x400'),null=True,blank=True)
    
    created_at=models.DateTimeField(auto_now_add = True)
    def __str__(self) -> str:
        return f"{self.vehicle} -- {self.created_at}"


# Note that Agency Class is just a profile of agency
# an Agency can have many branches, each have a different location and different rate
# after agency validation (Validate) a main branch gonna be created , related to this agency with same info
# Agency admin can create as mlany branches as he want
class Branch(models.Model):
    agency = models.ForeignKey(Agency,on_delete=models.CASCADE,related_name='my_branches')
    
    name = models.CharField(max_length=150)

    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True)
    
    # *** location ***
    # for now let's just make it very simple long, lat and address
    latitude = models.DecimalField(max_digits=50, decimal_places=30, null=True, blank=True)
    longitude = models.DecimalField(max_digits=50, decimal_places=30, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    wilaya = models.ForeignKey(Wilaya,on_delete = models.CASCADE,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_locked = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} - {self.agency.name}"

# ====== VEHICLE MODEL OPTIONS ======
# Make, Model, Type, Energy, Transmission, Options
class Make(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class Model(models.Model):
    make_id = models.ForeignKey(Make, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Model')
    series = models.CharField(max_length=100, help_text='Model', blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.name}'
    def get_vehicle_name(self):
        return f'{self.make_id.name} {self.name}'

class Type(models.Model):
    """Represent the type of vehicle"""
    name = models.CharField(max_length=100, help_text='Type of vehicle')
    def __str__(self) -> str:
        return self.name
    
class Energy(models.Model):
    name = models.CharField(max_length=50, help_text="Engine name")
    def __str__(self) -> str:
        return self.name

class Transmission(models.Model):
    name = models.CharField(max_length=20, help_text="Transmission name")
    def __str__(self) -> str:
        return self.name

class Option(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['name']

class Vehicle(models.Model):
    owned_by = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='my_vehicles')
    make=models.ForeignKey(Make,on_delete=models.SET_NULL,null=True)
    model=models.ForeignKey(Model,on_delete=models.SET_NULL,null=True)
    year=models.CharField(max_length=4)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_location=models.CharField(max_length=30,blank=True,null=True)
    engine = models.ForeignKey(Energy, on_delete=models.SET_NULL, null=True)
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    seats = models.PositiveSmallIntegerField(null=True, blank=True)
    doors = models.PositiveSmallIntegerField(null=True, blank=True)
    options = models.ManyToManyField(Option, blank=True)
    is_available=models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    description = models.TextField(max_length=1000, help_text='Small description (1000)', null=True, blank=True)

    # *** Pricing ***
    # Price can be diffirent per time
    # Price per day, Price per week, Price per month
    # => Default Price is per day
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_week = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # *** rental conditions ***
    min_rental_days = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text='Minimum number of rental days'
    )
    max_rental_days = models.PositiveSmallIntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
        help_text='Maximum number of rental days'
    )
    min_rental_age = models.PositiveSmallIntegerField(
        default=25,
        validators=[MinValueValidator(18)],
        help_text='Minimum age required to rent the vehicle'
    )
    is_fuel_full = models.BooleanField(
        default=False,
        help_text='Fuel status of the vehicle (True if full, False if not full)'
    )
    is_mileage_unlimited = models.BooleanField(
        default=False,
        help_text='Mileage status of the vehicle (True if unlimited, False if limited)'
    )
    is_with_driver = models.BooleanField(
        default=False,
        help_text='Indicates whether the vehicle is rented with a driver'
    )
    
    # ----- System ------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # *** Ordering ***
    class Meta:
        ordering = ['-created_at']

    # *** Methods ***
    def get_title(self):
        return f'{self.make} {self.model} {self.year}'
    def __str__(self) -> str:
        return self.get_title()

def vehicle_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'images/vehicles/{0}/{1}/{2}'.format(instance.vehicle.owned_by.name,instance.vehicle.id,filename)

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    url = models.URLField(default=('https://placehold.co/600x400'),null=True,blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add = True)
    def __str__(self) -> str:
        return f"{self.vehicle} -- {self.created_at}"
    class Meta:
        ordering = ['order']


# Ahh hell no,
# Why do I have to import Profile from api_main.models here not in the beginning
# => due to a circular import
# from api_main.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

# Reservation model
# connects agency, reserved vehicle, client
# status: accepted, refused, postponed
# Price: fixed [vehicle price per day * total_days(end_date - start_date)]
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('postponed', 'Postponed'),
    )
    
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE,related_name="my_reservations",null=True,blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE,related_name="reservations",null=True,blank=True)

    vehicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    client = models.ForeignKey(Profile, on_delete = models.CASCADE)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='postponed')
    total_days = models.PositiveSmallIntegerField(default=1)

    start_date = models.DateField()
    end_date = models.DateField()

    protection = models.BooleanField(default=False)
    protection_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Archived vehicle pricing
    vehicle_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # vehicle price * total_days 
    total_price_without_protection = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # total_price_without_protection + protection price
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Reservation by {self.client.first_name} for {self.vehicle.get_title()}"
    
    class Meta:
        ordering=['-created_at']

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        ordering=['-timestamp']
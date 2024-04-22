from django.db import models
from api_main.models import Profile
from api_auth.models import User
# the agency model just a profile of agency that can ber rolled by agency owner which is just a user with role agency_owner 
# the agency need to be validate by the admin (Platform Owner) to be able to use the system
class Agency(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='my_agency')
    is_validated = models.BooleanField(default=False)

    name = models.CharField(max_length=150, null=False, blank=False)
    bio = models.TextField(blank=True)
    
    # contact info
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)


    license_doc = models.ImageField(null=True,blank=True)
    photo = models.ImageField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    description = models.TextField(max_length=1000, help_text='Small description (1000)', null=True, blank=True)

    # price per day
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # System -----------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ordering
    class Meta:
        ordering = ['-created_at']

    # Methods
    def get_title(self):
        return f'{self.make} {self.model} {self.year}'
    
    # format price DZD
    def get_price(self):
        return f'{self.price} DZD'
    
    def __str__(self) -> str:
        return self.get_title()

def vehicle_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'images/vehicles/{0}/{1}/{2}'.format(instance.vehicle.owned_by.name,instance.vehicle.id,filename)

class VehicleImage(models.Model):
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to=vehicle_image_path)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.vehicle} -- {self.created_at}"


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
    
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE,related_name="my_reservations")
    vehicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    client = models.ForeignKey(Profile, on_delete = models.CASCADE)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='postponed')
    total_days = models.PositiveSmallIntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2,)

    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.email}'






class Agency(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,)
    name = models.CharField(max_length=150,null=False,blank=False)
    phone_number=models.CharField(max_length=14,)
    license_doc=models.ImageField(null=True,blank=True)
    photo=models.ImageField(null=True,blank=True)
    bio=models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.user}  {self.name}'
    
    def get_agency_name(self):
        return  f'{self.name}'


class Location(models.Model):
    Wilaya=models.CharField(max_length=200, blank=True)
    city=models.CharField(max_length=200, blank=True)
    street=models.CharField(max_length=200, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)





class Branch(models.Model):
    agency=models.ForeignKey(Agency,on_delete=models.CASCADE,)
    name=models.TextField(max_length=150)
    location=models.ForeignKey(Location,null=True,blank=True,on_delete=models.SET_NULL)
    rate=models.DecimalField(decimal_places=1,max_digits=1,default=0.0)

    def __str__(self) -> str:
        return f'{self.name}  by {self.agency.get_agency_name()}'

class Make(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Model(models.Model):
    make=models.ForeignKey(Make,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50)
    series = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self) -> str:
      return f'{self.make} {self.name} {self.series}' if self.series !='NULL' else f'{self.make} {self.name}'
     


class Type(models.Model):
    """Represent the type of vehicle"""
    name = models.CharField(max_length=100, help_text='Type of vehicle')
    def __str__(self) -> str:
        return self.name
    

# ------------------ Transmission ----------------------
class Transmission(models.Model):
    name = models.CharField(max_length=20, help_text="Transmission name")
    def __str__(self) -> str:
        return self.name
    

# ------------------ Options ----------------------
# (many to many relation with vehicle model)
class Option(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['name']


# ------------------ VehicleEngine ----------------------
class Energy(models.Model):
    name = models.CharField(max_length=50, help_text="Engine name")
    def __str__(self) -> str:
        return self.name



class Vehicle(models.Model):
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='my_cars')
    make=models.ForeignKey(Make,on_delete=models.SET_NULL,null=True)
    model=models.ForeignKey(Model,on_delete=models.SET_NULL,null=True)
    year=models.CharField(max_length=4)
    milage=models.IntegerField()
    current_location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    engine = models.ForeignKey(Energy, on_delete=models.SET_NULL, null=True)
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    seats = models.PositiveSmallIntegerField(null=True, blank=True)
    doors = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(max_length=1000, help_text='Small description (1000)', null=True, blank=True)
    # Options
    options = models.ManyToManyField(Option, related_name='vehicle', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='Vehicle price')
    
    # System -----------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    # Methods
    def get_price(self):
        return f'{self.price} DZD'

    def __str__(self) -> str:
        return f' {self.model}'
















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

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agency_owner', 'Agency Owner'),
        ('agency_admin', 'Agency Admin'),
        ('agency_employer', 'Agency Employer'),
        ('default', 'Default'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='default')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.email}'


# the agency model just a profile of agency that can ber rolled by agency owner which is just a user with role agency_owner 
# the agency need to be validate by the admin (Platform Owner) to be able to use the system
class Agency(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_validated = models.BooleanField(default=False)

    name = models.CharField(max_length=150,null=False,blank=False)
    phone_number=models.CharField(max_length=14,)
    bio=models.TextField(null=True,blank=True)

    license_doc=models.ImageField(null=True,blank=True)
    photo=models.ImageField(null=True,blank=True)



# Note that Agency Class is just a profile of agency
# an Agency can have many branches, each have a different location and different rate
# after agency validation (Validate) a main branch gonna be created , related to this agency with same info
# Agency admin can create as mlany branches as he want
class Branch(models.Model):
    agency=models.ForeignKey(Agency,on_delete=models.CASCADE,)
    name=models.TextField(max_length=150)
    location=models.CharField(max_length=30,null=True,blank=True)
    rate=models.DecimalField(decimal_places=1,max_digits=1,default=0)

class Make(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

# ------------------ VehicleModel  -----------------
class Model(models.Model):
    make_id = models.ForeignKey(Make, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Model')
    series = models.CharField(max_length=100, help_text='Model', blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.make_id.name} {self.name}'
    def get_vehicle_name(self):
        return f'{self.make_id.name} {self.name}'

class Type(models.Model):
    """Represent the type of vehicle"""
    name = models.CharField(max_length=100, help_text='Type of vehicle')
    def __str__(self) -> str:
        return self.name
    

# ------------------ VehicleEngine ----------------------
class Energy(models.Model):
    name = models.CharField(max_length=50, help_text="Engine name")
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


class Vehicle(models.Model):
    owned_by = models.OneToOneField(Branch, on_delete=models.CASCADE, related_name='my_cars')
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
    # Options
    options = models.ManyToManyField(Option, blank=True)


    description = models.TextField(max_length=1000, help_text='Small description (1000)', null=True, blank=True)

    
    price = models.DecimalField(max_digits=8, decimal_places=2,)
    # System -----------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    


    # Ordering
    class Meta:
        ordering = ['-created_at']

    # Methods
    def get_title(self):
        return f'{self.model.get_vehicle_name()} {self.year}'
    def get_price(self):
        return f'{self.price} DZD'
    
    def __str__(self) -> str:
        return self.get_title()
    











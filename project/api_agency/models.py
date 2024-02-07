from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_agency = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Agency(User):
    name = models.CharField(max_length=150,null=False,blank=False)
    phone_number=models.CharField(max_length=14,)
    license_doc=models.ImageField(null=True,blank=True)
    photo=models.ImageField(null=True,blank=True)
    bio=models.TextField(null=True,blank=True)




class Branch(models.Model):
    agency=models.ForeignKey(Agency,on_delete=models.CASCADE,)
    name=models.TextField(max_length=150)
    location=models.CharField(max_length=30,null=True,blank=True)
    rate=models.DecimalField(decimal_places=1,max_digits=1)

class Make(models.Model):
    name=models.CharField(max_length=50)

class Model(models.Model):
    make=models.ForeignKey(Make,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50)

class Vehicle(models.Model):
    make=models.ForeignKey(Make,on_delete=models.SET_NULL,null=True)
    model=models.ForeignKey(Model,on_delete=models.SET_NULL,null=True)
    year=models.CharField(max_length=4)
    milage=models.IntegerField()
    current_location=models.CharField(max_length=30,blank=True,null=True)






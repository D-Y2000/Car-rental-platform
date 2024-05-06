from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin


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
        super_user= self.create_user(email, password, **extra_fields)
        super_user.role='admin'
        super_user.save()
        return super_user

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=30,null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agency_admin', 'Agency Admin'),
        ('branch_admin', 'Branch Admin'),
        ('default', 'Default'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='default')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    def get_user_full_name(self):
        return f"{self.first_name} -- {self.last_name}"
    

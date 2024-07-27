from django.db import models
import datetime
from django.contrib.auth import get_user_model
from datetime import date
User = get_user_model()

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True,blank=True)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=GENDER_CHOICES, default="male")
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)



    # ===================== Custom Methods =====================
    def get_age(self):
        now = datetime.date.today()
        age = now.year - self.date_of_birth.year - ((now.month, now.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age


    def __str__(self) -> str:
        return f'{self.first_name}  {self.last_name}'
    
        


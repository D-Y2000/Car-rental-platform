from django.db import models
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # format date to dd-mm-yy 
    date_of_birth = models.DateField(null=True, blank=True)
    
    profile_image = models.ImageField(null=True,blank=True)

    def get_age(self):
        now = datetime.date.today()
        age = now.year - self.date_of_birth.year - ((now.month, now.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age


    def __str__(self) -> str:
        return f'{self.first_name}  {self.last_name}'
    
        


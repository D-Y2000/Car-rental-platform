from django.db import models
from api_agency.models import User,Agency
import datetime



# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(null=True,blank=True)

    def get_age(self):
        now =datetime.date.now()
        return now - self.date_of_birth 

    def __str__(self) -> str:
        return f'{self.first_name}  {self.last_name}'
    
        


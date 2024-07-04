from django.db import models
from api_agency.models import Wilaya
from api_auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


# class Category(models.Model):
#     name = models.CharField(max_length=30)


class Destination (models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    latitude = models.DecimalField(max_digits=50, decimal_places=30, null=True, blank=True)
    longitude = models.DecimalField(max_digits=50, decimal_places=30, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    wilaya = models.ForeignKey(Wilaya,on_delete = models.CASCADE,null=True,blank=True)
    rate = models.FloatField(default=0)

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    url = models.URLField(default=('https://placehold.co/600x400'),null=True,blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add = True)
    def __str__(self) -> str:
        return f"{self.destination} -- {self.created_at}"
    class Meta:
        ordering = ['order']

class Rate(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='destinations_ratings')
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name="destination_ratings")
    rate  = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=1.0)

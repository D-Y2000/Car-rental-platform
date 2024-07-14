from django.db import models
from api_agency.models import Wilaya
from api_main.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class ActivityCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)


class Activity(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='activities')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=50, decimal_places=30, null=True, blank=True)
    longitude = models.DecimalField(max_digits=50, decimal_places=30, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    wilaya = models.ForeignKey(Wilaya,on_delete = models.SET_NULL,null=True,blank=True)
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL,null=True, related_name='activities')
    rate  = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['-rate']

class ActivityImage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='images')
    url = models.URLField(default=('https://placehold.co/600x400'),null=True,blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add = True)
    def __str__(self) -> str:
        return f"{self.activity} -- {self.created_at}"
    class Meta:
        ordering = ['order']



class ActivityRate(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='activities_ratings')
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,related_name="activity_ratings")
    rate  = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)], default=1.0)


class ActivityFeedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='activities_feedbacks')
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Feedback from {self.user} for {self.activity}"
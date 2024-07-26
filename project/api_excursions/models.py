from django.db import models
from django.contrib.auth import get_user_model
from api_agency.models import Wilaya

# Create your models here.

# AUTH_USER_MODEL
User = get_user_model()

class ExcursionOrganizer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo_url = models.URLField(null=True, blank=True)
    # Todo add contact info

class Option(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['name']

class Excursion(models.Model):
    organizer = models.ForeignKey(ExcursionOrganizer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    options = models.ManyToManyField(Option, blank=True)

    starting_point = models.ForeignKey('Destination', on_delete=models.CASCADE, related_name='starting_point')
    ending_point = models.ForeignKey('Destination', on_delete=models.CASCADE, related_name='ending_point')
    starting_date = models.DateTimeField(blank=True)
    ending_date = models.DateTimeField(blank=True)

    # Todo add images
    # Todo add reviews

    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

# This model is used to store the destinations of an excursion (only)
class Destination(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='destinations')
    wilaya = models.foreignKey(Wilaya, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.excursion.title} - {self.wilaya.name} - {self.order}'
    
    class Meta:
        unique_together = ('excursion', 'order') # ma3natha mykonch fiha duplicated destination m3a same order
        ordering = ['order']

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from api_agency.models import Wilaya

# Create your models here.

# AUTH_USER_MODEL
User = get_user_model()

class ExcursionOrganizer(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='excursion_organizer')
    name = models.CharField(max_length=100)
    logo_url = models.URLField(null=True, blank=True)
    # Todo add contact information

# This model "Location" is global
# Todo change the location of this model to another app for a better organization
class Location(models.Model):
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, related_name='my_locations', blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True) #Optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.wilaya.name}'
    def getTitle(self):
        return f'{self.wilaya.name}'

class Excursion(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(ExcursionOrganizer, on_delete=models.CASCADE, related_name='excursions')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    starting_date = models.DateTimeField(blank=True, null=True)
    ending_date = models.DateTimeField(blank=True, null=True)

    locations = models.ManyToManyField(Location, through='ExcursionLocation')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)

    # Todo add a field for the duration of the excursion
    # Todo add images
    # Todo add options (like lunch, dinner, etc)
    # Todo add reviews

    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

# This model is used to store the destinations of an excursion (only)
class ExcursionLocation(models.Model):
    MEETING_POINT = 'meeting' # ay bayna
    DROP_OFF_POINT = 'drop_off' # ay bayna
    DESTINATION = 'destination' # Represents the destinations of the excursion destination 1, 2, 3 and so on

    POINT_TYPE_CHOICES = [
        (MEETING_POINT, 'Meeting Point'),
        (DROP_OFF_POINT, 'Drop-off Point'),
        (DESTINATION, 'Destination'),
    ]

    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='excursion_locations')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='excursion_locations')
    point_type = models.CharField(max_length=20, choices=POINT_TYPE_CHOICES, default=DESTINATION)
    order = models.PositiveIntegerField(default=0)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['order']  # Ensures ordering by the 'order' field

    def __str__(self):
        return f"{self.excursion.title} - {self.location.getTitle()} ({self.get_point_type_display()})"

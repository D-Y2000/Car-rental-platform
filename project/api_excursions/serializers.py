from rest_framework import serializers
from .models import ExcursionOrganizer, Excursion

class ExcursionOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcursionOrganizer
        fields = ['id', 'owner', 'name', 'logo_url']
        read_only_fields = ['owner']  # 'owner' is read-only so it can bet set automaticly to the authenticated user


# *** Excursion Creation ***
# Multipple steps for easier testing and debugging, as well as simplifying the front-end integration process.
# Step 1 (initial step): creating an excursion with only the title and automatically setting the organizer from the authenticated user.
class ExcursionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['id', 'title', 'organizer']
        read_only_fields = ['organizer']


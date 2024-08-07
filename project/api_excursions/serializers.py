from rest_framework import serializers
from .models import ExcursionOrganizer, Excursion, Location, ExcursionLocation, ExcursionMedia
from api_agency.serializers import WilayaSerializer

class ExcursionOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcursionOrganizer
        fields = ['id', 'owner', 'name', 'logo_url', "contact_phone"]
        read_only_fields = ['owner']  # 'owner' is read-only so it can bet set automaticly to the authenticated user


# *** Excursion Creation ***
# Multipple steps for easier testing and debugging, as well as simplifying the front-end integration process.
# Step 1 (initial step): creating an excursion with only the title and automatically setting the organizer from the authenticated user.
class ExcursionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['id', 'title', 'organizer']
        read_only_fields = ['organizer']

# Step 2: Update Excursion Details
class ExcursionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['id', 'title', 'description', 'price', 'starting_date', 'ending_date', "places"]
        read_only_fields = ['organizer', 'id']

# Step 3: Add excursion locations: (meeting points and destinations) to an existing excursion.
class CreateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['wilaya', 'latitude', 'longitude', 'address']

class ReadLocationSerializer(serializers.ModelSerializer):
    wilaya = WilayaSerializer(read_only=True)
    class Meta:
        model = Location
        fields = ['wilaya', 'latitude', 'longitude', 'address']

class CreateExcursionLocationSerializer(serializers.ModelSerializer):
    location = CreateLocationSerializer()

    class Meta:
        model = ExcursionLocation
        fields = ['id', 'excursion', 'location', 'point_type', 'order', 'time']
        read_only_fields = ['excursion', 'id']
        
    def create(self, validated_data):
        # retrieve location data from request data
        location_data = validated_data.pop('location')
        # create a new location object and store the id
        location = Location.objects.create(**location_data)
        # create a new ExcursionLocation object with the location id
        excursion_location = ExcursionLocation.objects.create(location=location, **validated_data)
        return excursion_location
    
class ReadExcursionLocationSerializer(serializers.ModelSerializer):
    location = ReadLocationSerializer()

    class Meta:
        model = ExcursionLocation
        fields = ['id', 'excursion', 'location', 'point_type', 'order', 'time']
        read_only_fields = ['excursion', 'id']

class ExcursionMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcursionMedia
        fields = '__all__'
        read_only_fields = ['excursion']

class ExcursionDetailSerializer(serializers.ModelSerializer):
    meeting_points = serializers.SerializerMethodField()
    drop_off_points = serializers.SerializerMethodField()
    destinations = serializers.SerializerMethodField()
    organizer = ExcursionOrganizerSerializer()
    media = ExcursionMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Excursion
        fields = ['id', 'organizer', 'title', 'description', 'price', 'places', 'status', 'starting_date', 'ending_date', 'views_count', 'created_at', 'updated_at', 'meeting_points', 'destinations', 'drop_off_points', "media"]
        read_only_fields = ['id', 'views_count', 'created_at', 'updated_at', 'organizer', "media"]

    def get_meeting_points(self, obj):
        return ReadExcursionLocationSerializer(obj.excursion_locations.filter(point_type=ExcursionLocation.MEETING_POINT), many=True).data
    def get_drop_off_points(self, obj):
        return ReadExcursionLocationSerializer(obj.excursion_locations.filter(point_type=ExcursionLocation.DROP_OFF_POINT), many=True).data
    def get_destinations(self, obj):
        return ReadExcursionLocationSerializer(obj.excursion_locations.filter(point_type=ExcursionLocation.DESTINATION), many=True).data
    
# Last step => Publish the excursion
class ExcursionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Excursion
        fields = ['status']
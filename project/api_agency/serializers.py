from rest_framework import serializers
from api_agency.models import *
from api_auth.serializers import UserSerializer


class AgencySerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Agency
        fields=["id",
                "user",
                "name",
                "phone_number",
                "bio",
                "license_doc",
                "photo",
                "email",
                "location",
                "address",
                "website",
                "is_validated",
                "created_at",
                ]
    
    def create(self, validated_data):
        #user account creation
        user_data=validated_data.pop('user')
        user=UserSerializer.create(self,user_data)
        user.role='agency_admin'
        user.save()
        validated_data['user']=user
        #agency creation
        agency=Agency.objects.create(**validated_data)
        agency.save()
        #create a branch for the agency
        branch=Branch.objects.create(agency=agency,name=f'{agency.name} branch')
        branch.save()

        return agency
    
class AgencyDetailSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Agency
        fields=["id",
                "user",
                "name",
                "phone_number",
                "bio",
                "license_doc",
                "photo",
                "email",
                "location",
                "address",
                "website",
                "is_validated",
                "created_at",
                ]

class LocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=50, decimal_places=30)
    lng = serializers.DecimalField(max_digits=50, decimal_places=30)

class BranchSerializer(serializers.ModelSerializer):
    agency=AgencySerializer(read_only=True)
    location = LocationSerializer(write_only=True,required=False)
    class Meta:
        model=Branch
        fields="__all__"
        

    def create(self, validated_data):
        user = self.context['request'].user
        agency = Agency.objects.get(user=user)
        validated_data['agency'] = agency

        branch = Branch.objects.create(**validated_data)
        
        # *** Add location ***
        # Set location manually
        # Note that location in frontend like this => {...prevdata, location:{lat: 36.8065, lng: 10.1815}}
        # location_data = validated_data.pop('location', {})
        # branch.latitude = location_data.get('lat', None)
        # branch.longitude = location_data.get('lng', None)

        branch.save()
        return branch
    
    def update(self, instance, validated_data):
        print("** UPDATE ** VALIDATED DATA:", validated_data)
        # *** Update location ***
        location_data = validated_data.pop('location', {})
        instance.latitude = location_data.get('lat', instance.latitude)
        instance.longitude = location_data.get('lng', instance.longitude)

        instance.save()
        return super().update(instance, validated_data)
    
        
class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=VehicleImage
        fields="__all__"
    
class VehicleSerializer(serializers.ModelSerializer):
    owned_by=BranchSerializer(read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length = 1000000, allow_empty_file=True, use_url = False),
        allow_empty=True,
        required=False,
        write_only=True)
    class Meta:
        model=Vehicle
        fields="__all__"
        extra_fields=["uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.get('uploaded_images', [])
        #check if there are images uploaded if so remove them from the validated data to create vehicle
        if uploaded_images:
            validated_data.pop("uploaded_images")
        user=self.context['request'].user
        agency=Agency.objects.get(user=user)
        branch=Branch.objects.filter(agency=agency)
        validated_data['owned_by']=branch.first()
        #check if there are options in the validated data 
        options=validated_data.get('options', [])
        if options:
            #extract options from validated data
            validated_data.pop('options')
        vehicle=Vehicle.objects.create(**validated_data)
        #set the options manually because it is a many to many relation
        vehicle.options.set(options)
        vehicle.save()
        if uploaded_images:
            for image in uploaded_images:
                newvehicle_image = VehicleImage.objects.create(vehicle=vehicle, image=image)
                newvehicle_image.save()
        return vehicle
        
    def update(self, instance, validated_data):
        uploaded_images = validated_data.get('uploaded_images', [])
        #check if there are images uploaded if so remove them from the validated data to create vehicle
        if uploaded_images:
            validated_data.pop("uploaded_images")
        if uploaded_images:
            for image in uploaded_images:
                newvehicle_image = VehicleImage.objects.create(vehicle=instance, image=image)
                newvehicle_image.save()

        #check if there are options in the validated data 
        options=validated_data.get('options', [])
        if options:
            #extract options from validated data
            validated_data.pop('options')
            instance.options.set(options)
        instance.save()

        return super().update(instance, validated_data)




class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields="__all__"

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields="__all__"


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields=['id','name']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields=['id','name']

class EnergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Energy
        fields=['id','name']

class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transmission
        fields=['id','name']



class VehicleDetailsSerializer(serializers.ModelSerializer):
    make=MakeSerializer()
    model=ModelSerializer()
    engine=EnergySerializer
    transmission=TransmissionSerializer()
    type=TypeSerializer()
    options=TypeSerializer(many=True)
    owned_by=BranchSerializer(read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    class Meta:
        model=Vehicle
        fields="__all__"




from api_main.serializers import ProfileDetailsSerializer

# Reservation serializer that allows the agencies to display thier reservations and can only accept or decline 

class AgencyReservationDetailsSerializer(serializers.ModelSerializer):
    agency=AgencyDetailSerializer(read_only=True)
    vehicle=VehicleDetailsSerializer(read_only=True)
    client=ProfileDetailsSerializer(read_only=True)
    start_date=serializers.DateField(read_only=True)
    end_date=serializers.DateField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model = Reservation
        fields = "__all__"

#Agency over view (readOnly)

class OverviewBranchSerializer(serializers.ModelSerializer):
    my_vehicles=VehicleDetailsSerializer(many=True,read_only=True)
    class Meta:
        model=Branch
        exclude = ['agency']



class OverviewAgencySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    my_branches=OverviewBranchSerializer(many=True,read_only=True)
    my_reservations=AgencyReservationDetailsSerializer(many=True,read_only=True)


    class Meta:
        model=Agency
        fields="__all__"
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


class BranchSerializer(serializers.ModelSerializer):
    agency=AgencySerializer(read_only=True)
    class Meta:
        model=Branch
        fields="__all__"

    def create(self, validated_data):
        user=self.context['request'].user
        agency=Agency.objects.get(user=user)
        validated_data['agency']=agency
        branch=Branch.objects.create(**validated_data)
        branch.save()
        return branch
        
class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=VehicleImage
        fields="__all__"
    
class VehicleSerializer(serializers.ModelSerializer):
    make=serializers.StringRelatedField
    model=serializers.StringRelatedField
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
        vehicle=Vehicle.objects.create(**validated_data)
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
        return super().update(instance, validated_data)


class VehicleDetailsSerializer(serializers.ModelSerializer):
    make=serializers.StringRelatedField()
    model=serializers.StringRelatedField()
    engine=serializers.StringRelatedField()
    transmission=serializers.StringRelatedField()
    type=serializers.StringRelatedField()
    options=serializers.StringRelatedField(many=True)
    owned_by=BranchSerializer(read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    class Meta:
        model=Vehicle
        fields="__all__"



class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields="__all__"

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
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
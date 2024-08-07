from django.forms import ValidationError
from django.utils import timezone

from rest_framework import serializers

from api_agency.models import *
from api_auth.serializers import UserSerializer
from payments.serializers import ListNewSubscriptionSerializer

class AgencySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # access only the last subscription of the agency
    # Note: > this is old version of my_subscriptions
    my_subscriptions = serializers.SerializerMethodField()
    def get_my_subscriptions(self, obj):
        last_subscription = obj.my_subscriptions.order_by('-created_at').first()
        if last_subscription:
            return SubscriptionSerializer(last_subscription).data
        return None
    
    # Note: > this is the updated version of my_subscriptions is becoming my_new_subscriptions
    # the serializer can be found in payments.serialisers
    my_new_subscriptions = serializers.SerializerMethodField()
    def get_my_new_subscriptions(self, obj):
        last_subscription = obj.my_new_subscriptions.order_by('-created_at').first()
        if last_subscription:
            return ListNewSubscriptionSerializer(last_subscription).data
        return None
    

    # A boolean field to indecate if the agency is in pro plan
    is_pro = serializers.SerializerMethodField()
    def get_is_pro(self, obj):
        # get last subscription
        last_subscription = obj.my_new_subscriptions.order_by('-created_at').first()
        # check if last subscription is Pro plan and valid
        if last_subscription:
            now = timezone.now()
            # check if Pro and time valid and status paid
            # the status is trigred by a webhook > check payments.views > webhook 
            return (
                last_subscription.plan.name == "Pro" and
                last_subscription.end_at is not None and
                last_subscription.end_at > now and
                last_subscription.status == "paid"
            )
        return False
    
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
                "rate",
                "created_at",
                "my_subscriptions",
                "my_new_subscriptions",
                "is_pro"
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
            
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Plan
        fields=["id",
                "name",
                "price",
                "max_vehicles",
                "max_branches",
                "unlimited_vehicles",
                "unlimited_branches",
                ]

class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Subscription
        fields=['plan']       

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = Subscription
        fields = ["id",
                "plan",
                "created_at",
                "end_at",
                ]
                  
class AgencyDetailSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    
    # access only the last subscription of the agency
    # Note: > this is old version of my_subscriptions
    my_subscriptions = serializers.SerializerMethodField()
    def get_my_subscriptions(self, obj):
        last_subscription = obj.my_subscriptions.order_by('-created_at').first()
        if last_subscription:
            return SubscriptionSerializer(last_subscription).data
        return None
    
    # Note: > this is the updated version of my_subscriptions is becoming my_new_subscriptions
    # the serializer can be found in payments.serialisers
    my_new_subscriptions = serializers.SerializerMethodField()
    def get_my_new_subscriptions(self, obj):
        last_subscription = obj.my_new_subscriptions.order_by('-created_at').first()
        if last_subscription:
            return ListNewSubscriptionSerializer(last_subscription).data
        return None
    

    # A boolean field to indecate if the agency is in pro plan
    is_pro = serializers.SerializerMethodField()
    def get_is_pro(self, obj):
        # get last subscription
        last_subscription = obj.my_new_subscriptions.order_by('-created_at').first()
        # check if last subscription is Pro plan and valid
        if last_subscription:
            now = timezone.now()
            # check if Pro and time valid and status paid
            # the status is trigred by a webhook > check payments.views > webhook 
            return (
                last_subscription.plan.name == "Pro" and
                last_subscription.end_at is not None and
                last_subscription.end_at > now and
                last_subscription.status == "paid"
            )
        return False
    
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
                "rate",
                "created_at",
                "my_subscriptions",
                "my_new_subscriptions",
                "is_pro"
                ]


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ["rate"]

    def create(self, validated_data):
        user =self.context['request'].user
        agency_pk = self.context['view'].kwargs.get('pk')
        try:
            agency=Agency.objects.get(pk=agency_pk)
            if Rate.objects.filter(user=user, agency=agency).exists():
                raise serializers.ValidationError("You have already rated this agency.")
            validated_data['user']=user
            validated_data['agency']=agency
            return super().create(validated_data)
        except Agency.DoesNotExist:
            raise serializers.ValidationError("Agency with ID {} does not exist".format(agency_pk))
        
class RateDetailsSerializer(serializers.ModelSerializer):
    # agency = AgencyDetailSerializer(many=False,read_only=True,)
    agency= serializers.SlugRelatedField(slug_field='name',read_only=True)
    user = UserSerializer(many=False,read_only=True)

    class Meta:
        model = Rate
        fields = "__all__"

class LocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=50, decimal_places=30)
    lng = serializers.DecimalField(max_digits=50, decimal_places=30)

class WilayaSerializer(serializers.ModelSerializer):
    class Meta :
        model = Wilaya
        fields="__all__"

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
        location_data = validated_data.pop('location', {})
        branch = Branch.objects.create(**validated_data)
        
        # *** Add location ***
        # Set location manually
        # Note that location in frontend like this => {...prevdata, location:{lat: 36.8065, lng: 10.1815}}
        
        branch.latitude = location_data.get('lat', None)
        branch.longitude = location_data.get('lng', None)

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
        
class BranchDetailsSerializer(serializers.ModelSerializer):
    agency=AgencySerializer(read_only=True)
    wilaya = WilayaSerializer()
    class Meta:
        model=Branch
        fields="__all__"

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=VehicleImage
        fields="__all__"
    
class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField(),  # Use JSONField to handle nested dict fields
        ),
        required=False,
        write_only=True
    )
    
    class Meta:
        model=Vehicle
        fields="__all__"
        extra_fields=["uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        options=validated_data.pop('options')

        vehicle = Vehicle.objects.create(**validated_data)
        vehicle.save()

        if options:
            vehicle.options.set(options)
         
        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                VehicleImage.objects.create(vehicle=vehicle, url=image_url, order = order).save()
        
        vehicle.save()

        return vehicle
        
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        options=validated_data.pop('options')

        if options:
            instance.options.set(options)
         
        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                VehicleImage.objects.create(vehicle=instance, url=image_url, order = order).save()
        
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
    engine=EnergySerializer()
    transmission=TransmissionSerializer()
    type=TypeSerializer()
    options=TypeSerializer(many=True)
    owned_by=BranchDetailsSerializer(read_only=True)
    images = VehicleImageSerializer(many=True, read_only=True)
    class Meta:
        model=Vehicle
        fields="__all__"

from api_main.serializers import ProfileDetailsSerializer

# Reservation serializer that allows the agencies to display thier reservations and can only accept or decline 
class AgencyReservationDetailsSerializer(serializers.ModelSerializer):
    agency=AgencyDetailSerializer(read_only=True)
    branch=BranchDetailsSerializer(read_only=True)
    vehicle=VehicleDetailsSerializer(read_only=True)
    client=ProfileDetailsSerializer(read_only=True)
    start_date=serializers.DateField(read_only=True)
    end_date=serializers.DateField(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model = Reservation
        fields = "__all__"

# OVERVIEW (AGENCY / BRANCH)
class OverviewBranchSerializer(serializers.ModelSerializer):
    my_vehicles = VehicleDetailsSerializer(many=True, read_only=True)    
    reservations = AgencyReservationDetailsSerializer(many=True, read_only=True)
    
    class Meta:
        model= Branch
        exclude = ['agency']

class OverviewAgencySerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    my_branches=OverviewBranchSerializer(many=True,read_only=True)
    my_reservations=AgencyReservationDetailsSerializer(many=True,read_only=True)


    class Meta:
        model=Agency
        fields="__all__"

class NotifcationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Notification
        fields = ["id","message","reservation","timestamp","is_read"]


class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Feedback
        fields = ["comment"]

    def create(self, validated_data):
        user = self.context['request'].user
        agency_pk = self.context['view'].kwargs.get('pk')
        try:
            agency=Agency.objects.get(pk=agency_pk)
            validated_data['user']=user
            validated_data['agency']=agency
            return super().create(validated_data)
        except Agency.DoesNotExist:
            raise serializers.ValidationError("Agency with ID {} does not exist".format(agency_pk))

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta : 
        model = Feedback
        fields = "__all__"

class CreateReportSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Report
        fields = ["issue"]
    def create(self, validated_data):
        user = self.context['request'].user
        agency_pk = self.context['view'].kwargs.get('pk')
        try:
            agency=Agency.objects.get(pk=agency_pk)
            validated_data['user']=user
            validated_data['agency']=agency
            return super().create(validated_data)
        except Agency.DoesNotExist:
            raise serializers.ValidationError("Agency with ID {} does not exist".format(agency_pk))

class ReportSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Report
        fields = "__all__"

class MonthlyReservationDataSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    reservation_count = serializers.IntegerField()

class DailyReservationDataSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    day = serializers.IntegerField()
    total_price = serializers.FloatField()
    reservation_count = serializers.IntegerField()
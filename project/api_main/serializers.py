from rest_framework import serializers
from api_main.models import Profile
from api_agency.serializers import UserSerializer,AgencyDetailSerializer,VehicleDetailsSerializer
from api_agency.models import Reservation

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields = '__all__'

    def create(self, validated_data):
        #user account creation
        user_data=validated_data.pop('user')
        user=UserSerializer.create(self,user_data)
        user.role='default'
        user.save()
        validated_data['user']=user
        #user_profile creation
        user_profile=Profile.objects.create(**validated_data)
        user_profile.save()
        

        return user_profile
    

class ProfileDetailsSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    client=ProfileDetailsSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = "__all__"

    def create(self, validated_data):
        profile=Profile.objects.get(user=self.context['request'].user)
        validated_data['client']=profile
        resrvation=Reservation.objects.create(**validated_data)
        resrvation.save()
        return resrvation

#client reservation serializer to display or update the reservation
class ClientReservationDetailsSerializer(serializers.ModelSerializer):
    agency=AgencyDetailSerializer(read_only=True)
    vehicle=VehicleDetailsSerializer()
    client=ProfileDetailsSerializer(read_only=True)
    status=serializers.CharField(read_only=True)
    class Meta:
        model = Reservation
        fields = "__all__"
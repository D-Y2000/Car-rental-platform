from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from api_auth.models import User
from api_auth.serializers import UserDetailsSerializer
from api_agency.models import Branch,Reservation
from api_agency.serializers import WilayaSerializer
from api_destination.models import Destination
from api_activity.models import Activity
class AdminUserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password],required = False)
    password2 = serializers.CharField(write_only=True,required = False)

    class Meta:
        model = User
        fields=["id","first_name","last_name"]

    
    def validate(self, attrs):
        if attrs.get('password'):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    
    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
            validated_data.pop('password','password2')
        return super().update(instance, validated_data)
    

class AdminBranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = "__all__"


class AdminReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"


class AdminDestinationSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    wilaya = WilayaSerializer()
    class Meta:
        model = Destination
        fields = "__all__"


class AdminActivitySerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    wilaya = WilayaSerializer()
    class Meta:
        model = Activity
        fields = "__all__"


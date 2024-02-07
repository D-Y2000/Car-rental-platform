from rest_framework import serializers
from api_agency.models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class AgencySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
     required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    class Meta:
        model=Agency
        fields=["id","name","email","phone_number","bio","license_doc","photo","password","password2"]
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        agency=Agency.objects.create(**validated_data)
        agency.set_password(validated_data['password'])
        agency.is_agency=True
        agency.save()
        return agency


class AgencyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Agency
        fields=["name","email","phone_number","bio","license_doc","photo",]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields="__all__"
        
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields="__all__"



from rest_framework import serializers
from api_agency.models import *
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
     required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    class Meta:
        model=User
        fields=["id","email","password","password2"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        user=User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user



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
        token =  self.context['request'].auth
        user=User.objects.get(auth_token=token)
        agency=Agency.objects.get(user=user)
        validated_data['agency']=agency
        branch=Branch.objects.create(**validated_data)
        branch.save()
        return branch
        
class VehicleSerializer(serializers.ModelSerializer):
    make=serializers.StringRelatedField
    model=serializers.StringRelatedField
    owned_by=BranchSerializer(read_only=True)
    class Meta:
        model=Vehicle
        fields="__all__"

    def create(self, validated_data):
        token =  self.context['request'].auth
        user = user=User.objects.get(auth_token=token)
        agency=Agency.objects.get(user=user)
        branch=Branch.objects.filter(agency=agency)
        validated_data['owned_by']=branch.first()
        vehicle=Vehicle.objects.create(**validated_data)
        vehicle.save()
        return vehicle

class VehicleDetailsSerializer(serializers.ModelSerializer):
    make=serializers.StringRelatedField()
    model=serializers.StringRelatedField()
    engine=serializers.StringRelatedField()
    transmission=serializers.StringRelatedField()
    type=serializers.StringRelatedField()
    options=serializers.StringRelatedField(many=True)
    owned_by=BranchSerializer(read_only=True)
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

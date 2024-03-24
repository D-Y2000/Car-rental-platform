from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from api_auth.models import User

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

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["id","first_name","last_name","email","role"]

from rest_framework import serializers
from api_activity.models import *
from api_main.serializers import UserSerializer

class ActivityCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityCategory
        fields = "__all__"
    
class LocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=50, decimal_places=30)
    lng = serializers.DecimalField(max_digits=50, decimal_places=30)



class ActivitySerializer(serializers.ModelSerializer):
    location = LocationSerializer(write_only=True,required=False)
    uploaded_images = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField(),  # Use JSONField to handle nested dict fields
        ),
        required=False,
        write_only=True
    )
    

    class Meta:
        model = Activity
        fields = "__all__"
        extra_fields=["uploaded_images"]

    def create(self, validated_data):
        # get the logged in user
        user = self.context['request'].user
        uploaded_images = validated_data.pop('uploaded_images')
        # add the user to the validated data to link it the activity 
        validated_data['user'] = user
        activity = Activity.objects.create(**validated_data)
        activity.save()

         
        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                ActivityImage.objects.create(activity = activity, url=image_url, order = order).save()
        
        activity.save()

        return activity


    def update(self, instance, validated_data):
        print("** UPDATE ** VALIDATED DATA:", validated_data)
        uploaded_images = validated_data.pop('uploaded_images')

        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                ActivityImage.objects.create(activity = instance, url=image_url, order = order).save()
        
        # *** Update location ***
        location_data = validated_data.pop('location', {})
        instance.latitude = location_data.get('lat', instance.latitude)
        instance.longitude = location_data.get('lng', instance.longitude)

        instance.save()
        return super().update(instance, validated_data)

class ActivityImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityImage
        fields = "__all__"

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityRate
        fields = ["rate"]

    def create(self, validated_data):
        user =self.context['request'].user
        activity_pk = self.context['view'].kwargs.get('pk')
        try:
            activity=Activity.objects.get(pk=activity_pk)
            activity_rate = ActivityRate.objects.get(user=user, activity=activity)
            if activity_rate:
                activity_rate = self.update(instance=activity_rate,validated_data=validated_data)
                activity_rate.save()
                return activity_rate
            validated_data['user']=user
            validated_data['activity']=activity
            return super().create(validated_data)
        except Activity.DoesNotExist:
            raise serializers.ValidationError("Activity with ID {} does not exist".format(activity_pk))
        
class RateDetailsSerializer(serializers.ModelSerializer):
    # activity = ActivityDetailSerializer(many=False,read_only=True,)
    activity= serializers.SlugRelatedField(slug_field='name',read_only=True)
    user = UserSerializer(many=False,read_only=True)

    class Meta:
        model = ActivityRate
        fields = "__all__"


class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta : 
        model = ActivityFeedback
        fields = ["comment"]

    def create(self, validated_data):
            user = self.context['request'].user
            activity_pk = self.context['view'].kwargs.get('pk')
            try:
                activity=Activity.objects.get(pk=activity_pk)
                validated_data['user']=user
                validated_data['activity']=activity
                return super().create(validated_data)
            except Activity.DoesNotExist:
                raise serializers.ValidationError("Activity with ID {} does not exist".format(activity_pk))



class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta : 
        model = ActivityFeedback
        fields = "__all__"

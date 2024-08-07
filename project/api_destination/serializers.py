from rest_framework import serializers
from api_destination.models import * 
from api_main.serializers import UserSerializer
# class CategorySerializer(serializers.ModelSerializer):

#     class Meta :
#         model = Category
#         fields = "__all__"


class LocationSerializer(serializers.Serializer):
    lat = serializers.DecimalField(max_digits=50, decimal_places=30)
    lng = serializers.DecimalField(max_digits=50, decimal_places=30)


class DestinationImageSerializer(serializers.ModelSerializer):
    location = LocationSerializer(write_only=True,required=False)

    class Meta : 
        model = DestinationImage
        fields = "__all__"



class DestinationSerializer(serializers.ModelSerializer):
    images = DestinationImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField(),  # Use JSONField to handle nested dict fields
        ),
        required=False,
        write_only=True
    )
    
    class Meta : 
        model = Destination
        fields = "__all__"
        extra_fields=["uploaded_images"]

    def create(self, validated_data):
        # get the logged in user
        user = self.context['request'].user
        uploaded_images = validated_data.pop('uploaded_images')
        # add the user to the validated data to link it the destination 
        validated_data['user'] = user
        destination = Destination.objects.create(**validated_data)
        destination.save()

         
        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                DestinationImage.objects.create(destination = destination, url=image_url, order = order).save()
        
        destination.save()

        return destination



    def update(self, instance, validated_data):
        print("** UPDATE ** VALIDATED DATA:", validated_data)
        uploaded_images = validated_data.pop('uploaded_images')

        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                DestinationImage.objects.create(destination = instance, url=image_url, order = order).save()
         
        # *** Update location ***
        location_data = validated_data.pop('location', {})
        instance.latitude = location_data.get('lat', instance.latitude)
        instance.longitude = location_data.get('lng', instance.longitude)

        instance.save()

        return super().update(instance, validated_data)



class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationRate
        fields = ["rate"]

    def create(self, validated_data):
        user =self.context['request'].user
        destination_pk = self.context['view'].kwargs.get('pk')
        try:
            destination=Destination.objects.get(pk=destination_pk)
            destination_rate = DestinationRate.objects.get(user=user, destination=destination)
            if destination_rate:
                destination_rate = self.update(instance=destination_rate,validated_data=validated_data)
                destination_rate.save()
                return destination_rate
            validated_data['user']=user
            validated_data['destination']=destination
            return super().create(validated_data)
        except Destination.DoesNotExist:
            raise serializers.ValidationError("Destination with ID {} does not exist".format(destination_pk))
        
   
class RateDetailsSerializer(serializers.ModelSerializer):
    destination= serializers.SlugRelatedField(slug_field='name',read_only=True)
    user = UserSerializer(many=False,read_only=True)

    class Meta:
        model = DestinationRate
        fields = "__all__"



class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta : 
        model = DestinationFeedback
        fields = ["comment"]

    def create(self, validated_data):
        user = self.context['request'].user
        destination_pk = self.context['view'].kwargs.get('pk')
        try:
            destination=Destination.objects.get(pk=destination_pk)
            validated_data['user']=user
            validated_data['destination']=destination
            return super().create(validated_data)
        except Destination.DoesNotExist:
            raise serializers.ValidationError("Destination with ID {} does not exist".format(destination_pk))

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta : 
        model = DestinationFeedback
        fields = "__all__"
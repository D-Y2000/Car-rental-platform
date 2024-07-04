from rest_framework import serializers
from api_destination.models import * 
from api_main.serializers import UserSerializer
# class CategorySerializer(serializers.ModelSerializer):

#     class Meta :
#         model = Category
#         fields = "__all__"


    

class DestinationImageSerializer(serializers.ModelSerializer):

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
        uploaded_images = validated_data.pop('uploaded_images')

        if uploaded_images:
            for image_data in uploaded_images:
                image_url = image_data.get('url')
                order = image_data.get('order')
                DestinationImage.objects.create(destination = instance, url=image_url, order = order).save()
        
        instance.save()

        return super().update(instance, validated_data)



class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ["rate"]

    def create(self, validated_data):
        user =self.context['request'].user
        destination_pk = self.context['view'].kwargs.get('pk')
        try:
            destination=Destination.objects.get(pk=destination_pk)
            if Rate.objects.filter(user=user, Destination=destination).exists():
                raise serializers.ValidationError("You have already rated this Destination.")
            validated_data['user']=user
            validated_data['destination']=destination
            return super().create(validated_data)
        except Destination.DoesNotExist:
            raise serializers.ValidationError("Destination with ID {} does not exist".format(destination_pk))
        
   
class RateDetailsSerializer(serializers.ModelSerializer):
    destination= serializers.SlugRelatedField(slug_field='name',read_only=True)
    user = UserSerializer(many=False,read_only=True)

    class Meta:
        model = Rate
        fields = "__all__"
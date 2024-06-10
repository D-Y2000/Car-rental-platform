from rest_framework import serializers

from api_agency.models import NewSubscription, Plan

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

class NewSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewSubscription
        fields = ['checkout_id', 'status', 'plan', 'agency']

class ListNewSubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = NewSubscription
        fields = ['checkout_id', 'status', 'plan', 'agency', 'created_at', 'end_at']
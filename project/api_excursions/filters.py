from django_filters import rest_framework as filters
from .models import Excursion, ExcursionLocation


class ExcursionFilter(filters.FilterSet):
    meeting_points = filters.CharFilter(method='filter_meeting_points')
    destinations = filters.CharFilter(method='filter_destinations')
    start_date = filters.DateFilter(field_name='starting_date', lookup_expr='gte')

    class Meta:
        model = Excursion
        fields = ["meeting_points", "destinations", "start_date"]

    def filter_meeting_points(self, queryset, name, value):
        return queryset.filter(
            excursion_locations__point_type=ExcursionLocation.MEETING_POINT,
            excursion_locations__location__wilaya__name__icontains=value
        )

    def filter_destinations(self, queryset, name, value):
        return queryset.filter(
            excursion_locations__point_type=ExcursionLocation.DESTINATION,
            excursion_locations__location__wilaya__name__icontains=value
        ) 
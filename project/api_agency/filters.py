import django_filters
from api_agency.models import Vehicle

class VehcilePriceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Vehicle
        fields = ['owned_by__wilaya','engine','transmission','type','options']

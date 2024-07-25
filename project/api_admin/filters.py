import django_filters
from api_agency.models import Reservation

class ClientAgeFilter(django_filters.FilterSet):
    # min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    # max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # client_age = django_filters.DateRangeFilter()

    class Meta:
        model = Reservation
        fields = ['branch__wilaya','client__gender']

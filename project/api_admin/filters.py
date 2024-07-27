import django_filters
from api_agency.models import Reservation
from datetime import date, timedelta
# class ClientAgeFilter(django_filters.FilterSet):
#     # min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
#     # max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
#     # client_age = django_filters.DateRangeFilter()

#     class Meta:
#         model = Reservation
#         fields = ['branch__wilaya','client__gender']




class ClientAgeFilter(django_filters.FilterSet):

    min_age = django_filters.NumberFilter(label='min_age', method = 'filter_by_min_age')
    max_age = django_filters.NumberFilter(label='max_age', method = 'filter_by_max_age')

    class Meta:
        model = Reservation
        fields = ['branch__wilaya','client__gender','status']

    def filter_by_min_age(self, queryset, name, value):
        today = date.today()
        print(f"today = {today}")
        min_birth_date = today - timedelta(days=int(value)*365)
        print(f"min_birth_date = {min_birth_date}")
        return queryset.filter(client__date_of_birth__gte=min_birth_date)

    def filter_by_max_age(self, queryset, name, value):
        today = date.today()
        print(f"today = {today}")
        max_birth_date = today - timedelta(days=(int(value))*365)
        print(f"max_birth_date = {max_birth_date}")
        return queryset.filter(client__date_of_birth__lte=max_birth_date)

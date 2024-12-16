import django_filters
from .models import Tour

class TourFilter(django_filters.FilterSet):
    operator_tour = django_filters.CharFilter(field_name='operator_tour', lookup_expr='icontains', label='Туроператор (поиск)')
    price_tour_min = django_filters.NumberFilter(field_name='price_tour', lookup_expr='gte', label='Минимальная цена')
    price_tour_max = django_filters.NumberFilter(field_name='price_tour', lookup_expr='lte', label='Максимальная цена')
    destination = django_filters.CharFilter(field_name='destination', lookup_expr='icontains', label='Место назначения')
    date_departure_after = django_filters.DateFilter(field_name='date_departure', lookup_expr='gte', input_formats=['%d.%m.%Y'], label='Дата отправления с')
    date_departure_before = django_filters.DateFilter(field_name='date_departure', lookup_expr='lte', input_formats=['%d.%m.%Y'], label='Дата отправления до')

    class Meta:
        model = Tour
        fields = [
            'operator_tour',
            'price_tour_min',
            'price_tour_max',
            'destination',
            'date_departure_after',
            'date_departure_before'
        ]

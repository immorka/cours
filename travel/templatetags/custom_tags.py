from django import template
from travel.models import Tour
from django.contrib.auth.models import AnonymousUser, User 
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_tours():
    return Tour.objects.count()

@register.simple_tag
def count_cheap_tours(max_price):
    """
    Возвращает количество туров, цена которых меньше указанного значения.
    """
    return Tour.objects.filter(price_tour__lt=max_price).count()

@register.simple_tag
def get_popular_destinations(limit=3):
    """
    Возвращает топ популярных направлений (сортировка по количеству туров).
    """
    return (
        Tour.objects.values('destination')
        .annotate(tour_count=Count('id'))
        .order_by('-tour_count')[:limit]
    )

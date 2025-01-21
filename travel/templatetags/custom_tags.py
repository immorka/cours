from django import template
from travel.models import Tour, Reservation
from django.contrib.auth.models import AnonymousUser, User 
from django.db.models import Count,F

register = template.Library()

@register.simple_tag
def total_tours():
    return Tour.objects.count()

@register.simple_tag
def count_cheap_tours(max_price):
    return Tour.objects.filter(price_tour__lt=max_price).count()

@register.simple_tag
def get_popular_destinations(limit=3):
    destinations = (
        Reservation.objects.values('id_tour__destination')
        .annotate(reservation_count=Count('id_tour'))
        .order_by('-reservation_count')[:limit]
    )

    for destination in destinations:
        tour_with_destination = Tour.objects.filter(destination=destination['id_tour__destination']).first()
        destination['image'] = tour_with_destination.image.url if tour_with_destination and tour_with_destination.image else None
        destination['url'] = f"/tours/?destination={destination['id_tour__destination']}" 
        destination['destination'] = destination['id_tour__destination']

    return destinations
@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
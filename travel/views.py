from rest_framework import viewsets
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock
from .serializers import (
    UserSerializer, TourSerializer, ReservationSerializer,
    ReviewSerializer, TravelHistorySerializer, FavoriteSerializer, StockSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class TravelHistoryViewSet(viewsets.ModelViewSet):
    queryset = TravelHistory.objects.all()
    serializer_class = TravelHistorySerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

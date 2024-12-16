from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from datetime import date
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock
from .serializers import (
    UserSerializer, TourSerializer, ReservationSerializer,
    ReviewSerializer, TravelHistorySerializer, FavoriteSerializer, StockSerializer
)
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TourFilter
from rest_framework.filters import SearchFilter

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

class ComplexTourQueryView(APIView):
    def get(self, request):
        min_price = int(request.query_params.get("min_price", 10000))
        max_price = int(request.query_params.get("max_price", 50000))
        departure_city = request.query_params.get("departure", "Москва")
        end_date = request.query_params.get("end_date", "2024-12-31")

        tours = Tour.objects.filter(
            Q(price_tour__gte=min_price) & Q(price_tour__lte=max_price) & Q(departure=departure_city) &
            Q(date_return__lte=end_date)
        ).exclude(operator_tour="Coral Travel")

        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)

class ComplexReservationQueryView(APIView):
    def get(self, request):
        from datetime import date
        from django.shortcuts import get_object_or_404
        from django.db.models import Q

        user_id = request.query_params.get("user_id", None)
        if not user_id:
            return Response({"error": "Отсуствует обязательный параметр user_id"}, status=400)

        user = get_object_or_404(User, id=user_id)
        today = date.today()

        reservations = Reservation.objects.filter(
            id_user=user
        ).filter(
            Q(status_pay=False) & Q(date_reservation__lt=today)
        ).exclude(
            id_tour__date_return__lt=today
        )

        paginator = PageNumberPagination()
        paginator.page_size = 5
        paginated_reservations = paginator.paginate_queryset(reservations, request)

        serializer = ReservationSerializer(paginated_reservations, many=True)
        return paginator.get_paginated_response(serializer.data)

class FilterByStatusView(APIView):
    def get(self, request, status):
        reservations = Reservation.objects.filter(status_pay=status)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TourFilter
    search_fields = ['name_tour', 'discription_tour']
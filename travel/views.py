from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Avg
from datetime import date
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock
from .serializers import (
    UserSerializer, TourSerializer, ReservationSerializer,
    ReviewSerializer, TravelHistorySerializer, FavoriteSerializer, StockSerializer
)
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404, render
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TourFilter
from rest_framework.decorators import action
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.contrib import messages 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, ReservationForm
from .models import Review
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.utils.timezone import now

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

        tours = Tour.objects.filter(Q(price_tour__gte=min_price) & Q(price_tour__lte=max_price) & Q(departure=departure_city) & Q(date_return__lte=end_date)).exclude(operator_tour="Coral Travel")

        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)

class ComplexReservationQueryView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)
        if not user_id:
            return Response({"error": "Отсуствует обязательный параметр user_id"}, status=400)

        user = get_object_or_404(User, id=user_id)
        today = date.today()

        reservations = Reservation.objects.filter(Q(id_user=user) & (Q(status_pay=False) | Q(payment_method="Банковская карта")) & ~Q(id_tour__date_return__lt=today))

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourFilter
  
    @action(methods=['get'], detail=False)
    def completed_tours(self, request):
        today = date.today()
        completed_tours = Tour.objects.filter(date_return__lt=today)
        serializer = self.get_serializer(completed_tours, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def tour_history(self, request, pk=None):
        tour = self.get_object()
        history = tour.history.all()

        history_data = []
        for record in history:
            history_data.append({
                "id": record.id,
                "name_tour": record.name_tour,
                "price_tour": record.price_tour,
                "operator_tour": record.operator_tour,
                "date_modified": record.history_date.strftime("%Y-%m-%d %H:%M:%S"),
                "modified_by": record.history_user.username if record.history_user else "System",
                "history_type": record.history_type,
            })

        return Response({
            "tour": tour.name_tour,
            "history": history_data
        })
    
class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(methods=['post'], detail=True)
    def change_status(self, request, pk=None):
        stock = self.get_object()
        new_status = request.data.get('status', None)

        if new_status not in ['true', 'false', 'True', 'False']:
            return Response({"error": "Статус должен быть 'true' или 'false'"}, status=400)

        stock.status_stock = new_status.lower() == 'true'
        stock.save()
        return Response({
            "message": f"Статус акции '{stock.name_stock}' изменен на '{'Активна' if stock.status_stock else 'Неактивна'}'."
        })

def index(request):
    hot_tours = Tour.objects.hot_tours()
    return render(request, 'travel/index.html', {'hot_tours': hot_tours})

def tours(request):
    sort_order = request.GET.get('sort', 'asc')
    if sort_order == 'desc':
        tours_list = Tour.objects.all().order_by('-price_tour')
    else:
        tours_list = Tour.objects.all().order_by('price_tour')

    paginator = Paginator(tours_list, 6)
    page = request.GET.get('page')

    try:
        tours = paginator.page(page)
    except PageNotAnInteger:
        tours = paginator.page(1)
    except EmptyPage:
        tours = paginator.page(paginator.num_pages)

    hot_tours = Tour.objects.hot_tours()
    cheap_tours = Tour.objects.cheap_tours(20000)
    average_price = Tour.objects.all().aggregate(Avg('price_tour'))['price_tour__avg']
    average_price = Tour.objects.all().aggregate(Avg('price_tour'))['price_tour__avg']
    if average_price:
        average_price = round(average_price)
        
    return render(request, 'travel/tours.html', {
        'tours': tours,
        'hot_tours': hot_tours,
        'cheap_tours': cheap_tours,
        'sort_order': sort_order,
        'average_price': average_price,
    })

def auth_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.name_user}!")
            return redirect('profile')
        else:
            messages.error(request, "Неправильный email или пароль.")
            return redirect('auth')

    return render(request, 'travel/auth.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if not name or not email or not password or not phone:
            messages.error(request, "Пожалуйста, заполните все поля.")
            return redirect('register')

        if User.objects.filter(email_user=email).exists():
            messages.error(request, "Этот email уже зарегистрирован.")
            return redirect('register')

        user = User.objects.create_user(
            name_user=name,
            email_user=email,
            password=password,
            number_user=phone,
            role_user="user",
            is_active=True
        )

        messages.success(request, "Вы успешно зарегистрировались! Теперь вы можете войти.")
        return redirect('auth')

    return render(request, 'travel/register.html')

@login_required
def profile_view(request):
    return render(request, 'travel/profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('auth')

def sorted_tours(request):
    tours = Tour.objects.all().order_by('price_tour')
    return render(request, 'travel/sorted_tours.html', {'tours': tours})

@login_required
def manage_reviews(request):
    reviews = Review.objects.filter(id_user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.id_user = request.user
            review.save()
            return redirect('manage_reviews')
    else:
        form = ReviewForm()
    return render(request, 'travel/manage_reviews.html', {'reviews': reviews, 'form': form})

@login_required
def edit_review_view(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review_text = request.POST.get('review_text')

        review = get_object_or_404(Review, id=review_id, id_user=request.user)
        review.text_review = review_text
        review.save()

        messages.success(request, "Отзыв успешно обновлен!")
        return redirect('manage_reviews')

    return redirect('manage_reviews')

@login_required
def delete_review(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review = get_object_or_404(Review, id=review_id, id_user=request.user)
        review.delete()
        messages.success(request, "Отзыв успешно удален.")
        return redirect('manage_reviews')

def tour_detail(request, id):
    tour = get_object_or_404(Tour, id=id)
    return render(request, 'travel/tour-detail.html', {'tour': tour})

@login_required
def reserve_tour(request):
    if request.method == 'POST':
        tour_id = request.POST.get('tour_id')
        payment_method = request.POST.get('payment_method')

        if not tour_id or not payment_method:
            return JsonResponse({"error": "Данные формы неполные. Проверьте отправку."}, status=400)

        tour = get_object_or_404(Tour, id=tour_id)

        if tour.places_tour <= 0:
            return JsonResponse({"error": "Нет доступных мест для этого тура."}, status=400)

        if Reservation.objects.filter(id_user=request.user, id_tour=tour).exists():
            return JsonResponse({"error": "Вы уже забронировали этот тур."}, status=400)

        reservation = Reservation.objects.create(
            id_user=request.user,
            id_tour=tour,
            date_reservation=now().date(),
            payment_method=payment_method,
            status_pay=False
        )

        tour.places_tour -= 1
        tour.save()

        return JsonResponse({"message": "Тур успешно забронирован!"}, status=200)

    return JsonResponse({"error": "Некорректный запрос."}, status=400)

@login_required
def user_reservations(request):
    reservations = Reservation.objects.select_related('id_tour').filter(id_user=request.user)
    return render(request, 'travel/user_reservations.html', {'reservations': reservations})

@login_required
def travel_history(request):
    history = TravelHistory.objects.prefetch_related('id_tour').filter(id_user=request.user)
    return render(request, 'travel/travel_history.html', {'history': history})
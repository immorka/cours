from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, TourViewSet, ReservationViewSet,
    ReviewViewSet, TravelHistoryViewSet, FavoriteViewSet, StockViewSet, ComplexTourQueryView, ComplexReservationQueryView, FilterByStatusView
)
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tours', TourViewSet)
router.register('reservations', ReservationViewSet)
router.register('reviews', ReviewViewSet)
router.register('travel-history', TravelHistoryViewSet)
router.register('favorites', FavoriteViewSet)
router.register('stocks', StockViewSet)

urlpatterns = router.urls + [
    path('complex-tours/', ComplexTourQueryView.as_view(), name='complex-tours'),
    path('complex-reservations/', ComplexReservationQueryView.as_view(), name='complex-reservations'),
    path('reservations/filter-by-status/<int:status>/', FilterByStatusView.as_view(), name='filter-by-status'),

]

from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, TourViewSet, ReservationViewSet,
    ReviewViewSet, TravelHistoryViewSet, FavoriteViewSet, StockViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tours', TourViewSet)
router.register('reservations', ReservationViewSet)
router.register('reviews', ReviewViewSet)
router.register('travel-history', TravelHistoryViewSet)
router.register('favorites', FavoriteViewSet)
router.register('stocks', StockViewSet)

urlpatterns = router.urls

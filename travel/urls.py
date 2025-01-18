from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    UserViewSet, TourViewSet, ReservationViewSet,
    ReviewViewSet, TravelHistoryViewSet, FavoriteViewSet, StockViewSet, ComplexTourQueryView, ComplexReservationQueryView, FilterByStatusView
)
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tours', TourViewSet)
router.register('reservations', ReservationViewSet)
router.register('reviews', ReviewViewSet)
router.register('travel-history', TravelHistoryViewSet)
router.register('favorites', FavoriteViewSet)
router.register('stocks', StockViewSet, basename='stocks')

urlpatterns = router.urls + [
    path('complex-tours/', ComplexTourQueryView.as_view(), name='complex-tours'),
    path('complex-reservations/', ComplexReservationQueryView.as_view(), name='complex-reservations'),
    path('reservations/filter-by-status/<int:status>/', FilterByStatusView.as_view(), name='filter-by-status'),
    path('', views.index, name='index'),
    path('tours/', views.tours, name='tours'),
    path('tour/<int:id>/', views.tour_detail, name='tour-detail'),
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', login_required(views.profile_view), name='profile'),
    path('my-reviews/', views.manage_reviews, name='manage_reviews'),
    path('my-reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('edit_review/', views.edit_review_view, name='edit_review'),
    path('delete_review/', views.delete_review, name='delete_review'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
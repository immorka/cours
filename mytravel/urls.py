from django.contrib import admin
from django.urls import path, include
from travel import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('travel.urls')),
    path('', views.index, name='index'),
    path('tours/', views.tours, name='tours'),
    path('tour/<int:id>/', views.tour_detail, name='tour-detail'),
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('sorted-tours/', views.sorted_tours, name='sorted_tours'),
    path('', include('travel.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
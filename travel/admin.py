from django.contrib import admin
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name_user", "email_user", "role_user")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("name_tour", "price_tour", "departure", "destination", "date_departure", "date_return")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour", "date_reservation", "status_pay", "payment_method")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour", "text_review")


@admin.register(TravelHistory)
class TravelHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour")


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("name_stock", "id_tour", "stock_value", "status_stock")
from django.contrib import admin
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name_user", "email_user", "role_user")
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("name_tour", "price_tour", "departure", "destination", "date_departure", "date_return")
    verbose_name = "Тур"
    verbose_name_plural = "Туры"

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour", "date_reservation", "status_pay", "payment_method")
    verbose_name = "Бронирование"
    verbose_name_plural = "Бронирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour", "text_review")
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"

@admin.register(TravelHistory)
class TravelHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour")
    verbose_name = "История поездок"
    verbose_name_plural = "Истории поездок"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour")
    verbose_name = "Избранное"
    verbose_name_plural = "Избранное"

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("name_stock", "id_tour", "stock_value", "status_stock")
    verbose_name = "Акция"
    verbose_name_plural = "Акции"
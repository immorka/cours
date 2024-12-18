from django.contrib import admin
from import_export.admin import ExportMixin
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock
from .resources import UserResource, TourResource, ReservationResource, StockResource
from django.utils import timezone
from import_export.formats.base_formats import XLSX

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1

@admin.register(User)
class UserAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = UserResource
    list_display = ("name_user", "email_user", "role_user")
    search_fields = ("name_user", "email_user") 
    list_filter = ("role_user",)
    fieldsets = (
        ("Личная информация", {"fields": ("name_user", "email_user", "number_user")}),
        ("Роли и доступ", {"fields": ("role_user", "password_user")}),
    )
    readonly_fields = ("email_user",)
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

@admin.register(Tour)
class TourAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TourResource
    formats = [XLSX]
    list_display = ("name_tour", "price_tour", "departure", "destination", "date_departure", "date_return","is_archived")
    list_filter = ("date_departure", "date_return", "operator_tour")
    search_fields = ("name_tour", "destination")
    actions = ["archive_old_tours"]
    inlines = [ReservationInline] 
    fieldsets = (("Основная информация", {"fields": ("name_tour", "discription_tour", "operator_tour")}),("Даты и места", {"fields": ("departure", "destination", "date_departure", "date_return")}),("Дополнительно", {"fields": ("price_tour", "places_tour")}),)
    verbose_name = "Тур"
    verbose_name_plural = "Туры"

    def is_archived(self, obj):
        return obj.operator_tour == "Архив"

    is_archived.boolean = True
    is_archived.short_description = "Заархивирован"

    def archive_old_tours(self, request, queryset):
        today = timezone.now().date()
        archived = queryset.filter(date_return__lt=today)
        count = archived.update(operator_tour="Архив")
        self.message_user(request, f"Архивировано {count} старых туров.")

    archive_old_tours.short_description = "Архивировать старые туры"

@admin.register(Reservation)
class ReservationAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ReservationResource
    list_display = ("id", "id_user", "id_tour", "date_reservation", "status_pay", "payment_method")
    list_filter = ("status_pay", "payment_method")
    search_fields = ("id_user__name_user", "id_tour__name_tour")
    verbose_name = "Бронирование"
    verbose_name_plural = "Бронирования"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour", "text_review")
    search_fields = ("id_user__name_user", "id_tour__name_tour")
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"

@admin.register(TravelHistory)
class TravelHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour")
    search_fields = ("id_user__name_user", "id_tour__name_tour")
    verbose_name = "История поездок"
    verbose_name_plural = "Истории поездок"

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour")
    search_fields = ("id_user__name_user", "id_tour__name_tour")
    verbose_name = "Избранное"
    verbose_name_plural = "Избранное"

@admin.register(Stock)
class StockAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = StockResource
    list_display = ("name_stock", "id_tour", "stock_value", "status_stock")
    list_filter = ("status_stock",)
    search_fields = ("name_stock", "id_tour__name_tour")
    actions = ["deactivate_all_stocks"]
    verbose_name = "Акция"
    verbose_name_plural = "Акции"

    def deactivate_all_stocks(self, request, queryset):
        count = queryset.update(status_stock=False)
        self.message_user(request, f"Деактивировано {count} акций.")

    deactivate_all_stocks.short_description = "Деактивировать выбранные акции"

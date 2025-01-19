from django.contrib import admin
from import_export.admin import ExportMixin
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock
from .resources import UserResource, TourResource, ReservationResource, StockResource
from django.utils import timezone
from import_export.formats.base_formats import XLSX
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.utils.translation import gettext_lazy as _
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1 
    fields = ('id_tour', 'date_reservation', 'payment_method', 'status_pay') 
    readonly_fields = ('id_tour', 'date_reservation', 'payment_method', 'status_pay')

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    fields = ('id_tour', 'text_review')
    readonly_fields = ('id_tour', 'text_review')

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 1
    fields = ('id_tour',)
    readonly_fields = ('id_tour',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email_user', 'name_user', 'number_user', 'role_user', 'is_staff', 'is_active')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email_user', 'name_user', 'number_user', 'role_user', 'is_staff', 'is_active')

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email_user', 'name_user', 'is_staff', 'is_active', 'role_user')
    list_filter = ('is_staff', 'is_active', 'role_user')

    fieldsets = (
        (None, {'fields': ('email_user', 'password')}),
        ('Персональная информация', {'fields': ('name_user', 'number_user', 'role_user')}),
        ('Права доступа', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email_user', 'password1', 'password2', 'name_user', 'number_user', 'role_user', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email_user', 'name_user')
    ordering = ('email_user',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data["password1"])
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)



@admin.register(Tour)
class TourAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = TourResource
    formats = [XLSX]
    list_display = ("name_tour", "price_tour", "departure", "destination", "date_departure", "date_return","is_archived","video_url")
    list_filter = ("date_departure", "date_return", "operator_tour")
    search_fields = ("name_tour", "destination")
    actions = ["archive_old_tours"]
    inlines = [ReservationInline] 
    fieldsets = (
        ("Основная информация", {"fields": ("name_tour", "discription_tour", "operator_tour", "image","video_url")}),
        ("Даты и места", {"fields": ("departure", "destination", "date_departure", "date_return")}),
        ("Дополнительно", {"fields": ("price_tour", "places_tour", "is_hot")}),)
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
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "id_user", "id_tour", "date_reservation", "status_pay", "payment_method")
    list_filter = ("status_pay", "payment_method")
    search_fields = ("id_user__name_user", "id_tour__name_tour")
    verbose_name = "Бронирование"
    verbose_name_plural = "Бронирования"

    actions = ["generate_pdf_report"]

    def generate_pdf_report(self, request, queryset):
        pdfmetrics.registerFont(TTFont('FreeSerif', 'static/fonts/FreeSerif.ttf'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont('FreeSerif', 12)
        p.drawString(100, 800, "Отчет о бронированиях")
        y = 750
        for reservation in queryset:
            text = f"Бронирование ID: {reservation.id}, Тур: {reservation.id_tour}, Пользователь: {reservation.id_user}, Оплата: {'Да' if reservation.status_pay else 'Нет'}"
            p.drawString(50, y, text)
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='reservation_report.pdf')

    generate_pdf_report.short_description = _("Сгенерировать PDF отчет")

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

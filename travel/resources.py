from import_export import resources, fields
from import_export.widgets import DateWidget
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'name_user', 'email_user', 'role_user', 'number_user')

class TourResource(resources.ModelResource):
    name_tour = fields.Field(
        column_name="Название тура",
        attribute="name_tour"
    )
    price_tour = fields.Field(
        column_name="Цена тура",
        attribute="price_tour"
    )
    departure = fields.Field(
        column_name="Место отправления",
        attribute="departure"
    )
    destination = fields.Field(
        column_name="Место назначения",
        attribute="destination"
    )
    date_departure = fields.Field(
        column_name="Дата отправления",
        attribute="date_departure",
        widget=DateWidget(format="%d-%m-%Y")
    )
    date_return = fields.Field(
        column_name="Дата возвращения",
        attribute="date_return",
        widget=DateWidget(format="%d-%m-%Y")
    )
    operator_tour = fields.Field(
        column_name="Туроператор",
        attribute="operator_tour"
    )

    class Meta:
        model = Tour
        fields = (
            "name_tour", "price_tour", "departure", "destination",
            "date_departure", "date_return", "operator_tour"
        )
        export_order = (
            "name_tour", "price_tour", "departure", "destination",
            "date_departure", "date_return", "operator_tour"
        )

class ReservationResource(resources.ModelResource):
    class Meta:
        model = Reservation
        fields = ('id', 'id_user__name_user', 'id_tour__name_tour', 'date_reservation', 'status_pay', 'payment_method')

class StockResource(resources.ModelResource):
    class Meta:
        model = Stock
        fields = ('id', 'name_stock', 'id_tour__name_tour', 'stock_value', 'status_stock')

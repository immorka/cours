from rest_framework import serializers
from .models import User, Tour, Reservation, Review, TravelHistory, Favorite, Stock
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
    def validate(self, data):
        if data['date_return'] < data['date_departure']:
            raise serializers.ValidationError({
                'date_return': "Дата возвращения должна быть позже даты отправления."
            })
        name_tour = data.get('name_tour')
        tour_id = self.instance.id if self.instance else None
        if Tour.objects.filter(name_tour=name_tour).exclude(id=tour_id).exists():
            raise serializers.ValidationError({
                'name_tour': "Тур с таким названием уже существует."
            })

        return data
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class TravelHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelHistory
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

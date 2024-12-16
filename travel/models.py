from django.db import models
from django.core.exceptions import ValidationError

def validate_positive(value):
    if value <= 0:
        raise ValidationError('Значение должно быть больше нуля.')

def validate_date_range(departure_date, return_date):
    if return_date < departure_date:
        raise ValidationError('Дата возвращения должна быть позже даты отправления.')
    
class User(models.Model):
    name_user = models.CharField("Имя пользователя", max_length=255)
    email_user = models.EmailField("Email пользователя", unique=True)
    role_user = models.CharField("Роль пользователя", max_length=50)
    password_user = models.CharField("Пароль пользователя", max_length=255)
    number_user = models.CharField("Номер телефона", max_length=15)

    def __str__(self):
        return self.name_user


class Tour(models.Model):
    name_tour = models.CharField("Имя пользователя", max_length=255)
    discription_tour = models.TextField("Описание тура")
    price_tour = models.IntegerField("Цена тура", validators=[validate_positive])
    departure = models.CharField("Место отправления", max_length=255)
    destination = models.CharField("Место назначения", max_length=255)
    date_departure = models.DateField("Дата отправления")
    date_return = models.DateField("Дата возвращения")
    operator_tour = models.CharField("Туроператор", max_length=255)
    places_tour = models.IntegerField("Количество мест", validators=[validate_positive])

    def clean(self):
        validate_date_range(self.date_departure, self.date_return)
        if Tour.objects.filter(name_tour=self.name_tour).exclude(id=self.id).exists():
            raise ValidationError('Тур с таким названием уже существует.')

    def __str__(self):
        return self.name_tour


class Reservation(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    date_reservation = models.DateField("Дата бронирования")
    status_pay = models.BooleanField("Статус оплаты")
    payment_method = models.CharField("Метод оплаты", max_length=50)

    def clean(self):
        if self.date_reservation < self.id_tour.date_departure:
            raise ValidationError('Дата бронирования не может быть раньше даты отправления.')

    def __str__(self):
        return f"Бронирование {self.id} от {self.id_user.name_user}"


class Review(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    text_review = models.TextField()

    def __str__(self):
        return f"Отзыв от {self.id_user.name_user} о {self.id_tour.name_tour}"


class TravelHistory(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)

    def __str__(self):
        return f"История: {self.id_user.name_user} - {self.id_tour.name_tour}"


class Favorite(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)

    def __str__(self):
        return f"Избранное: {self.id_user.name_user} - {self.id_tour.name_tour}"


class Stock(models.Model):
    name_stock = models.CharField("Название акции", max_length=255)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)
    stock_value = models.IntegerField("Размер скидки", validators=[validate_positive])
    status_stock = models.BooleanField("Статус акции")

    def __str__(self):
        return self.name_stock
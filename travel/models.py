from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.urls import reverse
from PIL import Image

def validate_positive(value):
    if value <= 0:
        raise ValidationError('Значение должно быть больше нуля.')
    
class User(models.Model):
    name_user = models.CharField("Имя пользователя", max_length=255)
    email_user = models.EmailField("Email пользователя", unique=True)
    role_user = models.CharField("Роль пользователя", max_length=50)
    password_user = models.CharField("Пароль пользователя", max_length=255)
    number_user = models.CharField("Номер телефона", max_length=15)

    def __str__(self):
        return self.name_user

class TourManager(models.Manager):
    def hot_tours(self):
        return self.filter(is_hot=True)

    def cheap_tours(self, max_price):
        return self.filter(price_tour__lte=max_price)
    
class Tour(models.Model):
    name_tour = models.CharField("Название тура", max_length=255)
    discription_tour = models.TextField("Описание тура")
    price_tour = models.IntegerField("Цена тура", validators=[validate_positive])
    departure = models.CharField("Место отправления", max_length=255)
    destination = models.CharField("Место назначения", max_length=255)
    date_departure = models.DateField("Дата отправления")
    date_return = models.DateField("Дата возвращения")
    operator_tour = models.CharField("Туроператор", max_length=255)
    places_tour = models.IntegerField("Количество мест", validators=[validate_positive])
    history = HistoricalRecords()
    is_hot = models.BooleanField(default=False)
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    objects = TourManager() 

    class Meta:
        ordering = ['date_departure']

    def __str__(self):
        return self.name_tour
    
    def get_absolute_url(self):
            return reverse('tour-detail', args=[self.id])
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img_path = self.image.path
            with Image.open(img_path) as img:
                if img.width > 350 or img.height > 250:
                    output_size = (350, 250)
                    img.thumbnail(output_size)
                    img.save(img_path)

class Reservation(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='reservations')
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE, related_name='reservations')
    date_reservation = models.DateField("Дата бронирования")
    status_pay = models.BooleanField("Статус оплаты")
    PAYMENT_METHODS = [('CARD', 'Банковская карта'), ('CASH', 'Наличные'), ('ONLINE', 'Онлайн оплата(СБП)')]
    payment_method = models.CharField("Метод оплаты", max_length=50, choices=PAYMENT_METHODS)

    def clean(self):
        if self.date_reservation < self.id_tour.date_departure:
            raise ValidationError('Дата бронирования не может быть раньше даты отправления.')

    def __str__(self):
        return f"Бронирование {self.id} от {self.id_user.name_user}"


class Review(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='reviews')
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE, related_name='reviews')
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
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE, related_name='stocks')
    stock_value = models.IntegerField("Размер скидки", validators=[validate_positive])
    status_stock = models.BooleanField("Статус акции")

    def __str__(self):
        return self.name_stock
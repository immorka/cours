from django.db import models
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords
from django.urls import reverse
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.timezone import now

def validate_positive(value):
    if value <= 0:
        raise ValidationError('Значение должно быть больше нуля.')
    
class UserManager(BaseUserManager):
    def create_user(self, email_user, password=None, **extra_fields):
        if not email_user:
            raise ValueError('Email обязателен для пользователя')
        email_user = self.normalize_email(email_user)
        user = self.model(email_user=email_user, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_user, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email_user, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email_user = models.EmailField("Email пользователя", unique=True)
    name_user = models.CharField("Имя пользователя", max_length=255)
    role_user = models.CharField("Роль пользователя", max_length=50)
    number_user = models.CharField("Номер телефона", max_length=15)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_user'
    REQUIRED_FIELDS = ['name_user']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

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
    video_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Ссылка на видеообзор"
    )
    class Meta:
        ordering = ['date_departure']
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

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
    date_reservation = models.DateField("Дата бронирования",default=now)
    status_pay = models.BooleanField("Статус оплаты",default=False)
    PAYMENT_METHODS = [('CARD', 'Банковская карта'), ('CASH', 'Наличные'), ('ONLINE', 'Онлайн оплата(СБП)')]
    payment_method = models.CharField("Метод оплаты", max_length=50, choices=PAYMENT_METHODS)
    document = models.FileField(
        upload_to='reservation_documents/',
        blank=True,
        null=True,
        verbose_name="Документ бронирования"
    )
    def clean(self):
        super().clean()

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"Бронирование {self.id} от {self.id_user.name_user}"


class Review(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='reviews')
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE, related_name='reviews')
    text_review = models.TextField()

    def clean(self):
        if not self.text_review or self.text_review.strip() == "":
            raise ValidationError({'text_review': 'Поле текста отзыва не может быть пустым.'})
        
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.id_user.name_user} о {self.id_tour.name_tour}"


class TravelHistory(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "История путешествий"
        verbose_name_plural = "Истории путешествий"

    def __str__(self):
        return f"История: {self.id_user.name_user} - {self.id_tour.name_tour}"


class Favorite(models.Model):
    id_user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"Избранное: {self.id_user.name_user} - {self.id_tour.name_tour}"


class Stock(models.Model):
    name_stock = models.CharField("Название акции", max_length=255)
    id_tour = models.ForeignKey(Tour, verbose_name="Тур", on_delete=models.CASCADE, related_name='stocks')
    stock_value = models.IntegerField("Размер скидки", validators=[validate_positive])
    status_stock = models.BooleanField("Статус акции")

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return self.name_stock
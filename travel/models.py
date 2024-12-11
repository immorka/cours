from django.db import models

class User(models.Model):
    name_user = models.CharField(max_length=255)
    email_user = models.EmailField(unique=True)
    role_user = models.CharField(max_length=50)
    password_user = models.CharField(max_length=255)
    number_user = models.CharField(max_length=15)

    def __str__(self):
        return self.name_user


class Tour(models.Model):
    name_tour = models.CharField(max_length=255)
    discription_tour = models.TextField()
    price_tour = models.IntegerField()
    departure = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    date_departure = models.DateField()
    date_return = models.DateField()
    operator_tour = models.CharField(max_length=255)
    places_tour = models.IntegerField()

    def __str__(self):
        return self.name_tour


class Reservation(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    date_reservation = models.DateField()
    status_pay = models.BooleanField()
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Reservation {self.id} by {self.id_user.name_user}"


class Review(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    text_review = models.TextField()

    def __str__(self):
        return f"Review by {self.id_user.name_user} for {self.id_tour.name_tour}"


class TravelHistory(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    def __str__(self):
        return f"History: {self.id_user.name_user} - {self.id_tour.name_tour}"


class Favorite(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_tour = models.ForeignKey(Tour, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite: {self.id_user.name_user} - {self.id_tour.name_tour}"


class Stock(models.Model):
    name_stock = models.CharField(max_length=255)
    id_tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    stock_value = models.IntegerField()
    status_stock = models.BooleanField()

    def __str__(self):
        return self.name_stock
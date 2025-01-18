from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tour, Reservation
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text_review', 'id_tour']
        widgets = {
            'text_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'id_tour': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_text_review(self):
        text_review = self.cleaned_data.get('text_review')
        if not text_review or text_review.strip() == "":
            raise forms.ValidationError("Отзыв не может быть пустым.")
        return text_review
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email_user', 'name_user', 'number_user', 'role_user', 'is_staff', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['payment_method']

    def clean_payment_method(self):
        payment_method = self.cleaned_data.get('payment_method')
        if not payment_method:
            raise ValidationError("Метод оплаты обязателен.")
        return payment_method
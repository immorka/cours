from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tour, Reservation
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

class ReviewForm(forms.ModelForm):
    clear_image = forms.BooleanField(
        required=False,
        label="Удалить изображение",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Review
        fields = ['text_review', 'id_tour', 'image']
        widgets = {
            'text_review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите ваш отзыв...',
            }),
            'id_tour': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'text_review': 'Текст отзыва',
            'id_tour': 'Тур',
            'image': 'Изображение',
        }
        help_texts = {
            'id_tour': 'Выберите тур, к которому относится отзыв.',
            'image': 'Вы можете загрузить изображение или удалить текущее.',
        }
    class Media:
        css = {
            'all': ('css/custom_form.css',)
        }
        js = ('js/custom_form.js',) 


    def save(self, commit=True, user=None):
        review = super().save(commit=False)
        if user:
            review.id_user = user
        if self.cleaned_data.get('clear_image') and review.image:
            review.image.delete(save=False)
            review.image = None
        if commit:
            review.save()
        return review

    def clean_text_review(self):
        text_review = self.cleaned_data.get('text_review')
        if "запрещённое слово" in text_review.lower():
            raise forms.ValidationError("Ваш отзыв содержит запрещённые слова.")
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
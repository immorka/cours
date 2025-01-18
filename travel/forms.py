from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['id_tour', 'text_review']
        widgets = {
            'id_tour': forms.Select(attrs={'class': 'form-control'}),
            'text_review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email_user', 'name_user', 'number_user', 'role_user', 'is_staff', 'is_active')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data["password1"])  # Хэшируем пароль
            user.save()
        return user

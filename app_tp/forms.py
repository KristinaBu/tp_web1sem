from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nickname']

    def clean(self):
        #проверка

        cleaned_data = super().clean()
        nickname = cleaned_data.get('nickname')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        email = cleaned_data.get('email')

        if username.strip() == '':
            raise ValidationError("Имя пользователя не может состоять только из пробелов")
        if password != password_repeat:
            raise ValidationError("Пароли не совпадают")
        if nickname.strip() == '':
            raise ValidationError("Никнейм не может состоять только из пробелов")
        if '@' not in email:
            raise ValidationError("Email должен содержать символ @")

        return cleaned_data




class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

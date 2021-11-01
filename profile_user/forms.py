from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
	username = forms.CharField(label="Логин",
	                           widget=forms.TextInput(attrs={'autofocus': True}))
	password = forms.CharField(label="Пароль", strip=False,
	                           widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}), )


class RegisterForm(UserCreationForm):
	"""
	Переопределяем стандартную форму регистрации
	"""
	
	username = forms.CharField(
			label="Логин",
			widget=forms.TextInput(attrs={"class": "form-class"}))
	first_name = forms.CharField(
			label="Имя",
			widget=forms.TextInput(attrs={"class": "form-class"}))
	last_name = forms.CharField(
			label="Фамилия",
			widget=forms.TextInput(attrs={"class": "form-class"}))
	email = forms.EmailField(
			label="Почта",
			widget=forms.EmailInput(attrs={"class": "form-class"}))
	password1 = forms.CharField(
			label="Пароль",
			widget=forms.PasswordInput(attrs={"class": "form-class"}))
	password2 = forms.CharField(
			label="Повтор пароля",
			widget=forms.PasswordInput(attrs={"class": "form-class"}))
	
	class Meta:
		# Установить связь с моделью БД
		model = User  # Стандартная модель в `django`
		# Какие поля нужно отобразить в форме
		fields = (
				"username",
				"first_name",
				"last_name",
				"email",
				"password1",
				"password2",
		)

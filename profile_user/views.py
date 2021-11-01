from typing import Any

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from profile_user.forms import RegisterForm, LoginUserForm


class ProfileView(LoginRequiredMixin, View):
	template_name = "profile_user/profile.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	login_url = reverse_lazy("login_user")  # Перенаправить на страницу если не авторизован
	
	# model = Profile # Какую модель используем
	# queryset = Profile.objects.all() # Получаем данные из БД
	
	def get(self, request: WSGIRequest):
		"""
		В методе обрабатывается GET запрос
		request.method == "GET"
		"""
		return render(request,
		              template_name=self.template_name,
		              context=self.get_context_data(), )
	
	def post(self, request: WSGIRequest, *args, **kwargs):
		"""
		В методе обрабатывается POST запрос
		request.method == "POST"
		"""
		...
	
	def get_context_data(self) -> dict[str, Any]:
		"""
		Сформировать контекст для шаблона `html`
		"""
		context = {
		}
		return context


class LoginUserView(LoginView):
	template_name = "profile_user/login_user.html"  # Путь к шаблону `html`
	form_class = LoginUserForm  # Форма аутентификации
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	
	def get_context_data(self, **kwargs) -> dict[str, Any]:
		"""
		Сформировать контекст для шаблона `html`
		"""
		return super().get_context_data(**kwargs)
	
	def get_success_url(self):
		"""
		При успешном входе перенаправить на указанную страницу
		"""
		return reverse_lazy("profile_user")


def logout_user(request: WSGIRequest):
	"""
	При выходе из профиля вся сессия отчищается !
	"""
	logout(request)  # Стандартная функция выхода
	return redirect("login_user")  # Перенаправить на страницу после выхода


class RegisterUserViewCreateView(CreateView):
	form_class = RegisterForm  # Наша форма регистрации
	template_name = "profile_user/register_user.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	success_url = reverse_lazy("profile_user")  # URL-адрес для перенаправления после успешной обработки формы.
	
	def get(self, request: WSGIRequest, *args, **kwargs):
		"""
		В методе обрабатывается GET запрос
		"""
		return super().get(request, *args, **kwargs)
	
	def post(self, request: WSGIRequest, *args, **kwargs):
		"""
		В методе обрабатывается POST запрос
		"""
		# Проверить данные, если они корректные то сохранить их в БД
		return super().post(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs) -> dict[str, Any]:
		"""
		В этом методе формировать `context` для шаблона `html`
		"""
		return super().get_context_data(**kwargs)
	
	def form_valid(self, form):
		"""
		Вызнается при успешной валидации формы
		"""
		user = form.save() # Сохраняем форму
		login(self.request, user) # Входим в профиль
		return redirect("profile_user") # Перенаправляем на станицу

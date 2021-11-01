from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View


class ProfileView(View):
	template_name = "profile_user/profile.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	
	# model = Prodile # Какую модель используем
	# queryset = Prodile.objects.all() # Получаем данные из БД
	
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
	
	def get_context_data(self, **kwargs) -> dict[str, Any]:
		"""
		Сформировать контекст для шаблона `html`
		"""
		context = {
		
		}
		return context

import random
from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from myapp.models import Product


class MainProductRibbon(ListView):
	"""
	Главная лента товаров
	"""
	
	model = Product  # Какую модель используем
	# queryset = Product.objects.all()  # Получаем данные из БД
	template_name = "myapp/MainProductRibbon.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	context_object_name = "MyPaginator"  # Для результата класса, Даем понятное имя переменой в шаблон.
	allow_empty = False  # Будет отображать ошибку 404 если страница не найдена
	
	paginate_by = 3  # Целое число, указывающее, сколько объектов должно отображаться на странице.
	ordering = "rating"  # Сортировать записи по указанному столбцу
	
	def get(self, request: WSGIRequest, *args, **kwargs):
		"""
		В методе обрабатывается GET запрос

		request.method == "GET"
		"""
		response = super().get(request, *args, **kwargs)
		
		if not request.COOKIES.get('hello'):
			response.set_cookie('hello', str(random.randint(0, 999)), max_age=5, secure=True)
		
		return response
	
	def get_context_data(self, **kwargs) -> dict[str, Any]:
		"""
		В этом методе формировать `context` для шаблона `html`
		"""
		context = super().get_context_data(**kwargs)
		# СВОЙ переменная, которую можно использовать для ограничения предложенных страниц
		context["max_offer_page"] = (-2, 2)
		return context


class ProductDetailView(DetailView):
	"""
	О товаре
	"""
	model = Product  # Какую модель используем
	# queryset = Product.objects.all()  # Получаем данные из БД
	template_name = "myapp/ProductDetailView.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	context_object_name = "product_obj"  # Для результата класса, Даем понятное имя переменой в шаблон.
	
	def get(self, request: WSGIRequest, *args, **kwargs):
		"""
		В методе обрабатывается GET запрос

		request.method == "GET"
		print(request.GET)
		"""
		
		resget = super().get(request, *args, **kwargs)
		return resget
	
	def get_context_data(self, **kwargs) -> dict[str, Any]:
		"""
		В этом методе формировать `context` для шаблон `html`
		"""
		context = super().get_context_data(**kwargs)
		return context


class Test(View):
	template_name = "myapp/test.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	
	# model =  # Какую модель используем
	# queryset = .objects. # Получаем данные из БД
	
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

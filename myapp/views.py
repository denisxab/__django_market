from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.views.generic import ListView, DetailView

from basket.views import BasketServer
from myapp.models import Product


class MainProductRibbon(ListView):
	"""
	Главная лента товаров
	"""
	
	model = Product  # Какую модель используем
	queryset = Product.objects.all()  # Получаем данные из БД
	template_name = "myapp/MainProductRibbon.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	context_object_name = "MyPaginator"  # Для результата класса, Даем понятное имя переменой в шаблон.
	allow_empty = False  # Отображать ошибку 404 если страница не найдена
	
	paginate_by = 3  # Целое число, указывающее, сколько объектов должно отображаться на странице.
	ordering = "price"  # Сортировать записи по столбцу
	
	def get(self, request: WSGIRequest, *args, **kwargs):
		"""
		В методе обрабатывается GET запрос

		request.method == "GfET"
		"""
		return super().get(request, *args, **kwargs)
	
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
	queryset = Product.objects.all()  # Получаем данные из БД
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

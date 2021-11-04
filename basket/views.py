from pprint import pprint
from typing import Any, Union, NamedTuple
import pydantic
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from myapp.models import Product


class BasketServer(View):
	"""
	Сервер для работы корзины с товарами
	"""
	
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	basket_name: str = "product_basket"  # Ключ для словаря в сессии
	model = Product  # Какую модель используем
	
	def get(self, request: WSGIRequest):
		"""
		В методе обрабатывается HEAD запрос

		request.method == "HEAD"
		"""
		# Отправляем корзину товаров.
		return HttpResponse(self.getBasketFromSession(request).json(), status=200)
	
	def post(self, request: WSGIRequest):
		# Флаг, который определяет действие сервера
		flag_product = request.POST.get('flag')
		"""
		Значение для флагов берутся из имени форм:
		- `basket.html` = payProduct (Купить товары)
		- `basket.html` = addProduct (Добавить товар в корзину)
		- `basket.html` = deleteProduct (Удалить товар из корзины)
		"""
		
		basket_json = self.getBasketFromSession(request)
		
		if flag_product == "payProduct":
			#  Оформляем заказ
			self._pay_product(basket_json)
		
		elif flag_product == "addProduct" or flag_product == "deleteProduct":
			# Получаем  id товара
			id_product: str = request.POST.get("selectIdProduct")
			
			if flag_product == "addProduct":
				# Если нужно добавить товар в корзину.
				self.add_product(basket_json, id_product)
			
			elif flag_product == "deleteProduct":
				# Если нужно удалить товар из корзины.
				self.delete_product(basket_json, id_product)
		
		# Сохраняем изменения в сессию пользователя.
		self.saveBasketInSession(basket_json, request)
		# Ответ клиенту.
		return HttpResponse(basket_json.json(), status=200)
	
	class Basket(pydantic.BaseModel):
		"""
		Структура корзины c товарами
		"""
		allProduct: int = 0
		content: dict[str, int] = {}
		
		@classmethod
		def session_parse_raw(cls, *args, **kwargs):
			"""
			Читаем данные из сессии, если они корректны, то десериализуем их,
			а если они не корректные, то создаем пустой объект.
			"""
			try:
				return cls.parse_raw(*args, **kwargs)
			except pydantic.error_wrappers.ValidationError:
				return cls(allProduct=0, content={})
		
		def addProductInBasket(self, _id_product: str):
			"""
			Добавляем товар в корзину
			"""
			product: Union[None, int] = self.content.get(_id_product, None)
			if product:
				# Если один и тот же товар добавляют в корзину, то добавляем в количество.
				self.content[_id_product] += 1
			else:
				self.content[_id_product] = 1  # Добавляем id товара в массив.
			self.allProduct += 1  # Прибавляем один товар в общее число товаров.
		
		def deleteProductInBasket(self, _id_product: str):
			product: Union[None, int] = self.content.get(_id_product, None)
			if product:
				# Если один и тот же товар добавляют в корзину, то добавляем в количество.
				self.content[_id_product] -= 1
				if self.content[_id_product] == 0:
					self.content.pop(_id_product)
				self.allProduct -= 1  # Прибавляем один товар в общее число товаров.
	
	class SendPayContent(NamedTuple):
		"""
		Структура для хранения оформленного заказа
		"""
		id_product: int
		name_product: str
		count_product: int
	
	def _pay_product(self, basket_json):
		# Получаем id товаров из сессии, чтобы найти их в БД
		list_key_basket_json = list(basket_json.content.keys())
		# Ищем товары по ID
		res_db = self.model.objects.filter(id__in=list_key_basket_json).order_by("-price")
		
		allPrice = 0  # Общая сумма покупки
		product = []  # Контент с товарами
		for _product in res_db:
			allPrice += _product.price * basket_json.content[str(_product.id)]
			product.append(
					self.SendPayContent(_product.id,
					                    _product.name_product,
					                    basket_json.content[str(_product.id)]))
		
		res = {
				"К Оплате": allPrice,
				"Товары"  : product,
		}
		pprint(res)
	
	@staticmethod
	def add_product(basket_json: Basket, id_product: str):
		# Добавляем товар в корзину.
		basket_json.addProductInBasket(id_product)
	
	@staticmethod
	def delete_product(basket_json: Basket, id_product: str):
		# Удалить товар из корзины.
		basket_json.deleteProductInBasket(id_product)
	
	def getBasketFromSession(self, request: WSGIRequest):
		# Получаем корзину из сессии.
		user_session: str = request.session.get(self.basket_name)
		# Десериализуем корзину.
		basket_json = self.Basket.session_parse_raw(user_session)
		return basket_json
	
	def saveBasketInSession(self, basket_json, request: WSGIRequest):
		# Сохраняем изменения в сессию пользователя.
		request.session[self.basket_name] = basket_json.json()


class BasketView(View):
	"""
	Страница с корзиной
	"""
	template_name = "basket/basket.html"  # Путь к шаблону `html`
	http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
	basket_name: str = "product_basket"  # Ключ для словаря в сессии
	
	def get(self, request: WSGIRequest):
		"""
		В методе обрабатывается GET запрос

		request.method == "GET"
		print(request.GET)
		"""
		return render(request,
		              template_name=self.template_name,
		              context=self.get_context_data(), )
	
	def get_context_data(self) -> dict[str, Any]:
		"""
		Сформировать контекст для шаблона `html`.
		"""
		tmp = self.request.session.get(self.basket_name)
		basket_json = BasketServer.Basket.session_parse_raw(tmp)
		
		list_key_basket_json = list(basket_json.content.keys())
		res_db = BasketServer.model.objects.filter(id__in=list_key_basket_json).order_by("-price")
		allPrice = 0
		all_product = []
		for _product in res_db:
			allPrice += _product.price * basket_json.content[str(_product.id)]
			all_product.append((_product, basket_json.content[str(_product.id)]))
		
		pprint(all_product)
		pprint(allPrice)
		
		context = {
				"basket"  : all_product,
				"allPrice": allPrice,
		}
		return context

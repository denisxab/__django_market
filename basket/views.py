import json
from pprint import pprint
from typing import Any, Union

import pydantic
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.urls import reverse
from django.views import View

from myapp.models import Product


class BasketServer(View):
    """
    Сервер для работы корзины с товарами
    """

    http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
    basket_name: str = "product_basket"  # Ключ для словаря в сессии

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

    def get(self, request: WSGIRequest):
        res = request.session.get(self.basket_name)
        tmp = self.Basket.parse_raw(res)
        return HttpResponse(tmp.json(), status=200)  # Отправляем данные о корзине товаров.

    def post(self, request: WSGIRequest, *args, **kwargs):
        """
        В методе обрабатывается POST запрос
        request.method == "POST".
        """
        res = b""
        id_product: str = request.POST.get("id-product")  # Получаем  id товара.
        user_session: str = request.session.get(self.basket_name)  # Получаем корзину из сессии.
        basket_json = self.Basket.session_parse_raw(user_session)  # Десериализуем корзину.

        # Флаг, который определяет добавить или удалить товар из корзины.
        flag_product = request.POST.get('flag')

        """
        Значение для флагов берутся из имени форм. 
        - `button_add_basket.html`
        - `button_delete_basket.html`
        """
        if flag_product == "AddProduct":
            """
            Если нужно добавить товар в корзину.
            """
            basket_json.addProductInBasket(id_product)  # Добавляем товар в корзину.
            res = json.dumps({
                "allProduct": basket_json.allProduct,  # Флаг добавления товара в корзину
                "flag": "append",  # Флаг удаления товара из корзины
                "selectIdProduct": id_product,  # Id выбранного товара
            })

        elif flag_product == "DeleteProduct":
            """
            Если нужно удалить товар в корзины.
            """
            basket_json.deleteProductInBasket(id_product)  # Удалить товар из корзины.
            res = json.dumps({
                "allProduct": basket_json.allProduct,  # Флаг добавления товара в корзину
                "flag": "delete",  # Флаг удаления товара из корзины
                "selectIdProduct": id_product,  # Id выбранного товара
            })

        pprint(basket_json)
        request.session[self.basket_name] = basket_json.json()  # Сохраняем массив в сессию пользователя.
        return HttpResponse(res, status=200)  # Отправляем количество товаров в корзине.

    @classmethod
    def get_context_data(cls, context):
        context["UrlBasketServer"] = reverse("basket_server")
        context["allProduct"] = "allProduct"
        context["NameFlagAppend"] = "append"
        context["NameFlagDelete"] = "delete"
        context["NameSelectId"] = "selectIdProduct"


class BasketView(View):
    """
    Страница с корзиной
    """
    template_name = "basket/basket.html"  # Путь к шаблону `html`
    http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
    model = Product  # Какую модель используем
    basket_name: str = "product_basket"  # Ключ для словаря в сессии

    def get(self, request: WSGIRequest, *args, **kwargs):
        """
        В методе обрабатывается GET запрос

        request.method == "GET"
        print(request.GET)
        """
        return render(request,
                      template_name=self.template_name,
                      context=self.get_context_data(), )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Сформировать контекст для шаблона `html`.
        """
        tmp = self.request.session.get(self.basket_name)
        basket_json = BasketServer.Basket.session_parse_raw(tmp)

        list_key_basket_json = list(basket_json.content.keys())
        res_db = self.model.objects.filter(id__in=list_key_basket_json).order_by("-price")
        allPrice = 0
        all_product = []
        for _product in res_db:
            allPrice += _product.price * basket_json.content[str(_product.id)]
            all_product.append((_product, basket_json.content[str(_product.id)]))

        pprint(all_product)
        pprint(allPrice)

        context = {
            "basket": all_product,
            "allPrice": allPrice,
        }

        BasketServer.get_context_data(context)  # Получить необходимый контекст для корзины

        return context

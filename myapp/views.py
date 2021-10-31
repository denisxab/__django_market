from pprint import pprint
from typing import Any, Union

import pydantic
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

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
        resget = super().get(request, *args, **kwargs)
        return resget

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        В этом методе формировать `context` для шаблона `html`

        :return: context
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
        :return: context
        """
        context = super().get_context_data(**kwargs)
        return context


class BasketView(View):
    template_name = "myapp/basket.html"  # Путь к шаблону `html`
    http_method_names = ["get", "post", ]  # Список методов HTTP, которые обрабатывает класс.
    model = Product  # Какую модель используем
    basket_name: str = "product_basket"  # Ключ для словаря в сессии

    class Basket(pydantic.BaseModel):
        """
        Структура корзины c товарами
        """
        AllProduct: int
        content: dict[str, int]

        @classmethod
        def session_parse_raw(cls, *args, **kwargs):
            """
            Читаем данные из сессии, если они корректны, то десериализуем их,
            а если они не корректные, то создаем пустой объект.
            """
            try:
                return cls.parse_raw(*args, **kwargs)
            except pydantic.error_wrappers.ValidationError:
                return cls(AllProduct=0, content={})

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
            self.AllProduct += 1  # Прибавляем один товар в общее число товаров.

        def deleteProductInBasket(self, _id_product: str):
            product: Union[None, int] = self.content.get(_id_product, None)
            if product:
                # Если один и тот же товар добавляют в корзину, то добавляем в количество.
                self.content[_id_product] -= 1
                if self.content[_id_product] == 0:
                    self.content.pop(_id_product)
                self.AllProduct -= 1  # Прибавляем один товар в общее число товаров.

    def get(self, request: WSGIRequest, *args, **kwargs):
        """
        В методе обрабатывается GET запрос

        request.method == "GET"
        print(request.GET)
        """
        return render(request,
                      template_name=self.template_name,
                      context=self.get_context_data(), )

    def post(self, request: WSGIRequest, *args, **kwargs):
        """
        В методе обрабатывается POST запрос
        request.method == "POST".
        """

        id_product: str = request.POST.get("id-product")  # Получаем  id товара.
        user_session: str = request.session.get(self.basket_name)  # Получаем корзину из сессии.
        basket_json = self.Basket.session_parse_raw(user_session)  # Десериализуем корзину.

        # Флаг, который определяет добавить или удалить товар из корзины.
        flag_product = request.POST.get('flag')

        """
        Значение для флагов берутся из имени форм. 
        - `button-add-basket.html`
        - `button-delete-basket.html`
        """
        if flag_product == "AddProduct":
            """
            Если нужно добавить товар в корзину.
            """
            basket_json.addProductInBasket(id_product)  # Добавляем товар в корзину.

        elif flag_product == "DeleteProduct":
            """
            Если нужно удалить товар в корзины.
            """
            basket_json.deleteProductInBasket(id_product)  # Удалить товар из корзины.

        pprint(basket_json)
        request.session[self.basket_name] = basket_json.json()  # Сохраняем массив в сессию пользователя.
        return HttpResponse(basket_json.AllProduct, status=200)  # Отправляем количество товаров в корзине.

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Сформировать контекст для шаблона `html`.
        """
        tmp = self.request.session.get(self.basket_name)
        basket_json = self.Basket.session_parse_raw(tmp)

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
        return context


# def form_test(request: WSGIRequest):
#     form = ProductForm.save_from_form(request)
#
#     context = {
#         "form": form[1]
#     }
#     print(form)
#     return render(request,
#                   template_name="myapp/form_test.html",
#                   context=context, )
#
#
# def home_fun(request: WSGIRequest):
#     context = {
#     }
#     return render(request,
#                   template_name="myapp/chaild.html",
#                   context=context, )
#
#
# def test_db(request: WSGIRequest):
#     x = Product.objects.all().order_by("-star").values("rating", "id")
#     y = x.values("id")
#     print(y)
#
#     context = {
#         "MyDataBase": x,
#         "MyDataBase2": y,
#
#     }
#     return render(request,
#                   template_name="myapp/test_db.html",
#                   context=context, )


class index_main(View):
    template_name = "myapp/index_main.html"  # Путь к шаблону `html`
    http_method_names = ["get", "post"]  # Список методов HTTP, которые обрабатывает класс.

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
            "ИмяИтератора": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        }
        return context

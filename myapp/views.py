from pprint import pprint
from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from myapp.forms import ProductForm
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

    basket_name = "basket_id"

    model = Product  # Какую модель используем

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
        request.method == "POST"
        """
        pprint(request.POST)
        request.session[BasketView.basket_name] = request.POST.get("id-product")
        return HttpResponse(f"{request.POST}",status=200)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Сформировать контекст для шаблона `html`
        """
        tmp = self.request.session.get(BasketView.basket_name)
        res = None
        if tmp:
            res = self.model.objects.get(pk=tmp)

        context = {
            "basket": res
        }
        return context


def form_test(request: WSGIRequest):
    form = ProductForm.save_from_form(request)

    context = {
        "form": form[1]
    }
    print(form)
    return render(request,
                  template_name="myapp/form_test.html",
                  context=context, )


def home_fun(request: WSGIRequest):
    context = {
    }
    return render(request,
                  template_name="myapp/chaild.html",
                  context=context, )


def test_db(request: WSGIRequest):
    x = Product.objects.all().order_by("-star").values("rating", "id")
    y = x.values("id")
    print(y)

    context = {
        "MyDataBase": x,
        "MyDataBase2": y,

    }
    return render(request,
                  template_name="myapp/test_db.html",
                  context=context, )


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

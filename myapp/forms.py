from typing import Tuple, Any

from django import forms
from django.core.handlers.wsgi import WSGIRequest

from .models import Product


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Пример установки параметров поля. Во время создания формы
        # self.fields['Имя'].Атрибут = "Значение"

    class Meta:
        """
        Класс отвечает за логику связи модели БД с формой.
        """

        # Установить связь с моделью БД
        model = Product

        # Какие поля нужно отобразить в форме
        fields = [
            "name_product",
            "shot_description",
            "star",
            "rating",
            "details_description", ]

        # Какие паля нужно исключить из формы
        # exclude = []

        # Если вам нужно задать атрибуты для html формы, то сделайте это здесь.
        widgets = {
            "name": forms.Textarea(attrs={"cols": 10, "rows": 1}),
        }

    @classmethod
    def save_from_form(cls, request: WSGIRequest, true_method="POST") -> Tuple[bool, Any]:
        """
        Метод для верификации и сохранения данных, из формы, в БД. Вызывать вручную.
        """
        """
        def index(request:WSGIRequest):
            form = AddPost.create_form(request)
            context = {"form": form[1], ... }
            return render(request, template_name="Name_app/Name.html", context=context, )
        """
        if request.method == true_method:  # Проверим метод запроса с необходимым методом
            form = cls(request.POST)  # Если метод подходящий, то создаем объект формы
            if form.is_valid():  # Проверим валидность данных из формы
                form.save()  # Если данные корректны, то сохранить данные в БД
                return True, ""  # Возвращаем заглушку
            return False, form  # Если валидация не пройдена, то вернем форму с сообщениями об ошибках
        else:
            return False, cls()  # Если метод не подходящий, то вернем форму для html шаблона

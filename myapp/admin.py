from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import NameDataBase, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name_product", "price", "star",
        "rating", "get_html_photo", )  # Имя столбца которые мы хотим видеть в админ панели
    list_display_links = ("name_product",)  # Указать имя столбца через которое можно перейти редактированию записи

    search_fields = ("name_product", "price")  # Указать по каким столбцам можно делать поиск

    list_editable = ("price", "star", "rating")  # Столбцы которые можно редактировать не открывая всю запись
    list_filter = ("price", "star", "rating")  # Столбцы, по которым можно фильтровать поиск
    save_on_top = False  # Панель с удаление/созданием записи вверху.

    date_hierarchy = "data_create"

    def get_html_photo(self, obj):
        """ Если нужно выводить мениатруы фоток """
        if obj.image_product:
            return mark_safe(f"<img src='{obj.image_product.url}' style='object-fit: contain;' width=150 height=150>")

    get_html_photo.short_description = "Миниатюра"

    # prepopulated_fields = {"slug": ("name",)}  # Авто заполнение слага URL на основе столбца

    readonly_fields = ("data_create",
                       "data_update",
                       "get_html_photo",
                       )  # Поля которые можно только смотреть, но не редактировать (нужно потом добавить в fields)

    fields = ("name_product",
              "price",
              "get_html_photo",
              "image_product",
              "star",
              "rating",
              "shot_description",
              "details_description",
              "data_create",
              "data_update",
              )  # Порядок отображения полей при редактировании записи


# редактирования

admin.site.register(NameDataBase)
# admin.site.register(Product, ProductAdmin)

# Register your models here.

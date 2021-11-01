
Подключить корзину к проекту
1. Используем модель Бд
    ```python
    class Product(models.Model):
        objects = None
        name_product = models.CharField(max_length=200,
                                        verbose_name="Имя товара",
                                        db_column="Имя товара", )
    
        price = models.IntegerField(validators=[MinValueValidator(0)], db_column="Цена", verbose_name="Цена",
                                    help_text="Цена")
    
        star = models.PositiveIntegerField(validators=[MaxValueValidator(5)], db_column="Звезды", verbose_name="Звезды",
                                           help_text="Звезды")
    
        rating = models.IntegerField(db_column="Рейтинг", verbose_name="Рейтинг", help_text="Рейтинг")
    
        shot_description = models.CharField(max_length=200,
                                            help_text="Краткое описание",
                                            verbose_name="Краткое описание",
                                            db_column="Краткое описание", )
    
        details_description = models.TextField(db_column="Полное описание",
                                               verbose_name="Полное описание",
                                               help_text="Полное описание", )
    
        image_product = models.ImageField(upload_to=f"photo/%Y/%m/%d/",  # Шаблон имени
                                          db_column="Фото товара",
                                          verbose_name="Фото товара",
                                          help_text="Фото товара", )
    
        data_create = models.DateField(db_column="Дата создания",
                                       verbose_name="Дата создания",
                                       auto_now_add=True)
        data_update = models.DateTimeField(db_column="Дата обновления",
                                           verbose_name="Дата обновления",
                                           auto_now=True)
    
        def __str__(self):
            """
            Для отображение в текстовом виде для админ панели, и консоли.
            """
            return str(self.name_product)
    
        def get_absolute_url(self):
            """
            Для получения ссылки записи в Html и отображение в админ панели.
            """
            return reverse("product", kwargs={"pk": self.pk})
    
        class Meta:
            """
            Вспомогательный класс для админ панели.
            """
            verbose_name = "Товар"  # Имя таблицы в единственном числе
            verbose_name_plural = "Товары"  # Имя таблицы во множественном числе
            ordering = ["-price", ]  # Сортировать записи по указанным столбцам (можно указывать несколько столбцов)
    ```

2. В главный `Html` шаблон добавить - `JavaScript` скрипты для корзины.
    ```html
    {% load basket_tag %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        {% BasketPlug  %}
    </head>
    ```
3. В главный `Html` шаблон добавить - Всплывающие окно корзины.
    ```html
    {% BasketWindow %}
    ```
4. Кнопка добавить в корзину. Передать уникальный ID записи из Бд
    ```html
    {% BasketButtonAddProduct product_obj.pk %}
    ```
5. Кнопка удалить из корзины. Передать уникальный ID записи из Бд
    ```html
    {% BasketButtonDeleteProduct product_obj.pk %}
    ```
5. Кнопка оформить заказ.
    ```html
    {% BasketButtonPayProduct %}
    ```
//   Когда `html`  документ  загружен, создаем  функцию  для  обработки  нажатия
$(document).ready(function () {
    // Перехватываем отправку формы
    $('.BasketForm').submit(function () {

        // Сериализуем данные из формы и имя формы.
        const dataVAr = $(this).serialize() + '&flag=' + $(this).attr('name') // !!!

        // Отладочная информация
        const infoObf = {
            data: $(this).serialize(),
            methed: $(this).attr('method'),
            action: $(this).attr('action'),
            name: $(this).attr('name'),
            datavar: dataVAr
        }
        console.log("Отправка формы", infoObf)

        // Отправляем `ajax` запрос
        $.ajax({
            // Тело сообщения
            method: $(this).attr('method'), // Берем метод из формы
            url: $(this).attr('action'), // Берем url из формы
            data: dataVAr, // Данные на сервер
            // Если при отправке возникли ошибки
            error: function (response) {
                const exceptionVar = `Ошибка отправки ${response}`
                alert(exceptionVar);
                console.error(exceptionVar)
            }
        }).done(function (msg) { // Получаем ответ от сервера, и обрабатываем его.
            const response_server = $.parseJSON(msg); // Десериализуем ответ

            console.log("Ответ сервера", response_server);

            if (response_server.flag == NameFlagDelete) {
                // Если удаляют товар, то выполняем логику по удалению товара рш
                deleteProduct(response_server[NameSelectId]);
                alert("Товар удален из корзины: " + response_server[NameFlagDelete]);
            } else if (response_server.flag == NameFlagAppend) {
                // Если добавляют товар, то выполняем логику по добавлению товара
                alert("Товар добавлен в корзину: " + response_server[allProduct]);
            }
            updateProductInBasket(response_server[allProduct]);

        });
        // Остановить перезагрузку страницы
        return false;
    });


    function updateBasket() {
        // Обновляем корзину товаров = Отправляем `ajax` запрос
        $.ajax({
            // Тело сообщения
            method: "get", // Метод для сервера
            url: UrlBasketServer, // Url адрес сервера

            // Если при отправке возникли ошибки
            error: function (response) {
                const exceptionVar = "Ошибка получения корзины от сервера" + response
                console.error(exceptionVar)
            }
        }).done(function (msg) {
            const response_server = $.parseJSON(msg); // Десериализуем ответ
            console.log("Ответ от сервера в корзину", response_server)
            updateProductInBasket(response_server[allProduct]);
            console.log("Корзина обновлена", response_server[allProduct]);
            document.getElementById("basket-box").hidden = false
            console.log("Корзина показана")
        })
    }

    updateBasket();
})


function updateProductInBasket(countProduct) {
    let elem = document.getElementById("countProductInBasket");
    elem.innerText = countProduct;
}

function getInfoProductIntId(idProduct) {
    // Получить значения товара по `id`
    let product = document.getElementById(idProduct);
    console.log("Товар", product);
    let infoBottom = product.getElementsByClassName("bottom-info-basket");

    console.log("Информация", infoBottom);

    let price = infoBottom[0].children[0].innerText;
    let count = infoBottom[0].children[1].innerText;
    let allPriceProduct = infoBottom[0].children[2].innerText;

    console.log("цена", price);
    console.log("штук", count);
    console.log("сумма", allPriceProduct);
}


function deleteProduct(idProduct) {
    // Удаление товара по `id`
    let product = document.getElementById(idProduct);
    console.log("Товар", product);

    let infoBottom = product.getElementsByClassName("bottom-info-basket");
    console.log("Информация", infoBottom);

    infoBottom[0].children[1].innerText -= 1;
    infoBottom[0].children[2].innerText = infoBottom[0].children[0].innerText * infoBottom[0].children[1].innerText

    if (infoBottom[0].children[1].innerText === '0') {
        console.log(`Удаление элемента ${idProduct}`);
        product.remove()
    }

    let price = infoBottom[0].children[0].innerText;
    let count = infoBottom[0].children[1].innerText;
    let allPriceProduct = infoBottom[0].children[2].innerText;

    console.log("цена", price);
    console.log("штук", count);
    console.log("сумма", allPriceProduct);
}
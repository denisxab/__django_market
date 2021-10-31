//   Когда `html`  документ  загружен, создаем  функцию  для  обработки  нажатия
$(document).ready(function () {
    // Перехватываем отправку формы
    $('.BasketForm').submit(function () {

        // Сериализуем данные из формы и имя формы.
        const dataVAr = $(this).serialize() + '&flag=' + $(this).attr('name')

        // Отладочная информация
        console.log("ClickButtonBasket : ")
        console.log($(this).serialize())
        console.log($(this).attr('method'))
        console.log($(this).attr('action'))
        console.log($(this).attr('name'))
        console.log(dataVAr)


        // Отправляем `ajax` запрос
        $.ajax({
            // Тело сообщения
            method: $(this).attr('method'), // Берем метод из формы
            url: $(this).attr('action'), // Берем url из формы
            data: dataVAr, // Данные на сервер


            // Если при отправке возникли ошибки
            error: function (response) {
                const exceptionVar = "Ошибка отправки" + response
                alert(exceptionVar);
                console.log(exceptionVar)
            }
        }).done(function (msg) { // Получаем ответ от сервера, и обрабатываем его.
            alert(msg)
            console.log(msg)
        });

        // Остановить перезагрузку страницы
        return false;
    });


})


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
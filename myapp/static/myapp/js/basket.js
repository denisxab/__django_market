//   Когда `html`  документ  загружен, создаем  функцию  для  обработки  нажатия
$(document).ready(function () {
    // Перехватываем отправку формы
    $('.BasketForm').submit(function () {
        // Отладочная информация
        console.log("ClickButtonBasket : ")
        console.log($(this).serialize())
        console.log($(this).attr('method'))
        console.log($(this).attr('action'))

        // Отправляем `ajax` запрос
        $.ajax({
            // Тело сообщения
            method: $(this).attr('method'), // Берем метод из формы
            url: $(this).attr('action'), // Берем url из формы
            data: $(this).serialize(), // Сереализуем данные из формы в json

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
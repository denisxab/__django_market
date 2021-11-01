//   Когда `html`  документ  загружен, создаем  функцию  для  обработки  нажатия
$(document).ready(function () {

	/*
    Форма запроса на сервер:
	{
	csrfmiddlewaretoken: ...:str,                    // Csrf Токен
	selectIdProduct: ...:int,                        // Id Выбранного товара
	flag: addProduct/deleteProduct/payProduct:str,   // Указание что сделать серверу
	}

    Форма ответа от сервера:
	{
	allProduct: ...:int,                          // Всего товаров в корзине
	content: {},
	}
    */

	$(".BasketFormPay").submit(function () {
		// Флаг для сервера
		const flag = "payProduct";
		// Оформить заказ
		[methodVar, urlVar, idProduct, dataSerial] = new GetFormPay(this, flag);

		// Запрос на сервер
		const Response = $.ajax({
			// Тело сообщения
			method: methodVar,
			url: urlVar,
			data: dataSerial,

			// Если при отправке возникли ошибки
			error: function (response) {
				const exceptionVar = `Ошибка отправки ${response}`;
				alert(exceptionVar);
				console.error(exceptionVar);
			}
		});

		// Обрабатываем ответ сервера
		Response.done(function (msg) {
			// Десериализуем ответ
			const response_server = $.parseJSON(msg);
			console.log("Ответ сервера", response_server);
			alert("Ваш заказ оформлен");
			ReloadPage();
		});

		// Остановить перезагрузку страницы
		return false;
	})


	$('.BasketFormAddProduct').submit(function () {
		// Флаг для сервера
		const flag = "addProduct";
		// Получаем необходимые данные из формы
		[methodVar, urlVar, idProduct, dataSerial] = new GetFormProduct(this, flag);


		// Запрос на сервер
		const Response = $.ajax({
			// Тело сообщения
			method: methodVar,
			url: urlVar,
			data: dataSerial,

			// Если при отправке возникли ошибки
			error: function (response) {
				const exceptionVar = `Ошибка отправки ${response}`;
				alert(exceptionVar);
				console.error(exceptionVar);
			}
		});

		// Получаем ответ от сервера, и обрабатываем его.
		Response.done(function (msg) {
			// Десериализуем ответ
			const response_server = $.parseJSON(msg);
			console.log("Ответ сервера", response_server);
			alert("Товар добавлен в корзину: " + idProduct);
			updateProductInBasket(response_server["allProduct"]);
		});

		// Остановить перезагрузку страницы
		return false;
	})

	// Перехватываем отправку формы
	$('.BasketFormDelete').submit(function () {
		// Флаг для сервера
		const flag = "deleteProduct";
		// Получаем необходимые данные из формы
		[methodVar, urlVar, idProduct, dataSerial] = new GetFormProduct(this, flag);

		// Запрос на сервер
		const Response = $.ajax({
			// Тело сообщения
			method: methodVar,
			url: urlVar,
			data: dataSerial,

			// Если при отправке возникли ошибки
			error: function (response) {
				const exceptionVar = `Ошибка отправки ${response}`;
				alert(exceptionVar);
				console.error(exceptionVar);
			}
		});

		// Получаем ответ от сервера, и обрабатываем его.
		Response.done(function (msg) {
			// Десериализуем ответ
			const response_server = $.parseJSON(msg);
			console.log("Ответ сервера", response_server);
			deleteProduct(idProduct);
			alert("Товар удален из корзины: " + idProduct);
			updateProductInBasket(response_server["allProduct"]);
		});

		// Остановить перезагрузку страницы
		return false;
	});

	function ReloadPage() {
		console.log("Js reload");
		window.location.reload();
	}

	function updateBasket() {
		/*
        Обновляем корзину товаров = Отправляем `ajax` запрос
        */
		$.ajax({
			// Тело сообщения
			method: "get", // Метод для сервера
			url: UrlBasketServer, // Url адрес сервера
			// Если при отправке возникли ошибки
			error: function (response) {
				const exceptionVar = "Ошибка получения корзины от сервера" + response;
				console.error(exceptionVar);
			}
		}).done(function (msg) {
			const response_server = $.parseJSON(msg); // Десериализуем ответ
			console.log("Ответ от сервера в корзину", response_server)
			updateProductInBasket(response_server["allProduct"]);
			console.log("Корзина обновлена", response_server["allProduct"]);
			document.getElementById("basket-box").hidden = false;
			console.log("Корзина показана");
		})
	}

	function GetFormProduct(_this, _flag) {
		// Метод формы
		const methodVar = $(_this).attr('method');
		// Url Сервера
		const urlVar = $(_this).attr('action');
		//  Id товара
		const idProduct = $(_this).find("[name=selectIdProduct]")[0].value;
		// Сериализуем данные из формы и имя формы.
		const dataSerial = $(_this).serialize() + '&flag=' + _flag;

		console.log("Флаг клиента", _flag);
		console.log("Метод формы", methodVar);
		console.log("Url", urlVar);
		console.log("ID товара", idProduct);
		console.log("Сериализованные данные", dataSerial);

		return [methodVar, urlVar, idProduct, dataSerial];
	}

	function GetFormPay(_this, _flag) {
		// Метод формы
		const methodVar = $(_this).attr('method');
		// Url Сервера
		const urlVar = $(_this).attr('action');
		// Сериализуем данные из формы и имя формы.
		const dataSerial = $(_this).serialize() + '&selectIdProduct=-1' + '&flag=' + _flag;

		console.log("Метод формы", methodVar);
		console.log("Флаг зароса", _flag);
		console.log("Url", urlVar);
		console.log("Сериализованные данные", dataSerial);

		return [methodVar, urlVar, -1, dataSerial];
	}

	// При загрузке документа обновить значения в `html` корзине
	updateBasket();

	function updateProductInBasket(countProduct) {
		/*

        Обновить данные в `html` корзине

        */
		let elem = document.getElementById("countProductInBasket");
		elem.innerText = countProduct;
	}

	function getInfoProductIntId(idProduct) {
		/*

        Получить товар по id

        */
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
		/*
        Удалить товар из корзины по id
        */

		// Получить товар по `id`
		let product = document.getElementById(idProduct);
		console.log("Товар", product);

		// Получить бокс с товаром
		let infoBottom = product.getElementsByClassName("bottom-info-basket");
		console.log("Весь блок", infoBottom);
		console.log("цена товара", infoBottom[0].children[0].innerText);
		console.log("штук", infoBottom[0].children[1].innerText);
		console.log("сумма", infoBottom[0].children[2].innerText);

		// Вычитаем количество
		infoBottom[0].children[1].innerText -= 1;
		// Вычитаем стоимость дублированных тавров
		infoBottom[0].children[2].innerText = infoBottom[0].children[0].innerText * infoBottom[0].children[1].innerText;
		// Уменьшение общей стоимости товаров в корзине
		document.getElementById("allPrice").innerText -= infoBottom[0].children[0].innerText;
		// Если количество товаров равно нулю то удаляем бокс
		if (infoBottom[0].children[1].innerText === '0') {
			console.log(`Удаление элемента ${idProduct}`);
			product.remove();
		}

		// Получаем количество тавров
		const lengthListProduct = document.getElementsByClassName("product-box").length;
		console.log("Длинна ленты", lengthListProduct);
		// Если товаров нет в корзине перенаправляем на домашнею страницу.
		if (lengthListProduct == "0") {
			ReloadPage();
		}
	}

	function deleteAllProduct() {

	}
})


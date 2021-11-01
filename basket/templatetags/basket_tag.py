from django import template

register = template.Library()


@register.inclusion_tag("basket/button_add_basket.html")
def BasketButtonAddProduct(id_product):
	return {"id_product": id_product}


@register.inclusion_tag("basket/button_delete_basket.html")
def BasketButtonDeleteProduct(id_product):
	return {"id_product": id_product}


@register.inclusion_tag("basket/button_pay_basket.html")
def BasketButtonPayProduct():
	return None


@register.inclusion_tag("basket/plug_basket.html")
def BasketPlug():
	return None


@register.inclusion_tag("basket/basket_box.html")
def BasketWindow():
	return None

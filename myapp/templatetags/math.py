from django import template

register = template.Library()


@register.simple_tag()
def tagSum(a, b, c):
	"""
	 {% tagSum %}
	"""
	return a + b + c


@register.inclusion_tag("myapp/testTag.html")
def tagInclusion(data1,data2):
	"""
	{% tagInclusion %}
	"""
	return {"data": [data1,data2]}


@register.filter
def multiply(value, arg):
	"""
	{{ quantity | multiply:price }}
	"""
	return value * arg

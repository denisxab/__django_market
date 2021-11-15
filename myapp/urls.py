from django.urls import path

from myapp.views import MainProductRibbon, ProductDetailView, Test

urlpatterns = [
		path('', MainProductRibbon.as_view(), name="main_lent"),
		path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
		path('test/', Test.as_view())
]

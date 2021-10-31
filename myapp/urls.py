from django.conf import settings
from django.urls import path, include

from myapp.views import MainProductRibbon, ProductDetailView, BasketView, BasketServer

urlpatterns = [
    path('', MainProductRibbon.as_view(), name="main_lent"),
    path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
    path('basket/', BasketView.as_view(), name="basket"),
    path('basket_server/', BasketServer.as_view(), name="basket_server"),
    path('class/', MainProductRibbon.as_view(), name="class_"),
]


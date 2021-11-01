from django.urls import path

from basket.views import BasketView, BasketServer

urlpatterns = [
    path('', BasketView.as_view(), name="basket"),
    path('basket_server/', BasketServer.as_view(), name="basket_server"),
]

from django.urls import path

from myapp.views import MainProductRibbon, ProductDetailView

urlpatterns = [
    path('', MainProductRibbon.as_view(), name="main_lent"),
    path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
    path('class/', MainProductRibbon.as_view(), name="class_"),
]

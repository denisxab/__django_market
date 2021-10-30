from django.conf import settings
from django.urls import path, include

from myapp.views import MainProductRibbon, home_fun, test_db, ProductDetailView, BasketView

urlpatterns = [
    path('', MainProductRibbon.as_view(), name="main_lent"),
    path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
    path('basket/', BasketView.as_view(), name="basket"),

    path('home/', home_fun, name="home"),
    path('db/', test_db, name="db"),
    # path('form/', NameCreateView.as_view(), name="form"),
    path('class/', MainProductRibbon.as_view(), name="class_"),
    # path('tpaginator/', MyPaginatorListView.as_view(), name="tpaginator"),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )

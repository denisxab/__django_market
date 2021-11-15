from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from myapp.views import MainProductRibbon, ProductDetailView

urlpatterns = [
		path('', MainProductRibbon.as_view(), name="main_lent"),
		path('product/<int:pk>', ProductDetailView.as_view(), name="product"),
]

# if settings.DEBUG:
# 	import debug_toolbar
# 	urlpatterns.append(
# 		path('__debug__/', include(debug_toolbar.urls)),
# 	)
from django.urls import path

from profile_user.views import ProfileView

urlpatterns = [
		path('', ProfileView.as_view(), name="profile_user"),
]

from django.urls import path

from profile_user.views import ProfileView, LoginUserView, RegisterUserViewCreateView, logout_user

urlpatterns = [
		path('', ProfileView.as_view(), name="profile_user"),
		path('login/', LoginUserView.as_view(), name="login_user"),
		path('logout/', logout_user, name="logout_user"),
		path('register/', RegisterUserViewCreateView.as_view(), name="register_user"),

]

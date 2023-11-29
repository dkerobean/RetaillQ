from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # noqa


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="user-register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('transactions/', views.TransactionView.as_view(), name="transactions"),

    path('profile/view/', views.UserProfileView.as_view(), name='profil-view'),

    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'), # noqa
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # noqa



]

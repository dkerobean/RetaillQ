from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="user-register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('transactions/', views.TransactionView.as_view(), name="transactions"),

    path('profile/view/', views.UserProfileView.as_view(), name='profil-view'),

    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='custom-token-obtain-pair'),  # Use the custom view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # noqa



]

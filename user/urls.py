from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # noqa


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="user-register"),
    path('transactions/', views.TransactionView.as_view(), name="transactions"),

    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'), # noqa
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # noqa


]

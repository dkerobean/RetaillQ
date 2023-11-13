from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # noqa


urlpatterns = [
    path('register/', views.RegisterationView.as_view(), name="user-register"),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # noqa
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # noqa


]

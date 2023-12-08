from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.SalesView.as_view(), name="sale"),
    path('all/<int:pk>/', views.SalesView.as_view(), name="sale-detail"),
    path('<int:pk>/', views.SalesView.as_view(), name="sale-singlr"),
]

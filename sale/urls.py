from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.SalesView.as_view(), name="sale"),
]

from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.ProductsView.as_view(), name="products"),
    path('single/<int:pk>/', views.ProductView.as_view(), name="single-product"),
    path('list/<int:pk>/', views.ProductsView.as_view(), name="product-detail"),


]

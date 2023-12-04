from django.urls import path
from .views import ProductsView


urlpatterns = [
    path('products/', ProductsAPIView.as_view(), name="products"),
    path('products/<int:pk>', ProductsAPIView.as_view(), name="product-detail"),

]

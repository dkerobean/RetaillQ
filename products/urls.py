from django.urls import path
from .views import ProductsView


urlpatterns = [
    path('list/', ProductsView.as_view(), name="products"),
    path('list/<int:pk>/', ProductsView.as_view(), name="product-detail"),

]

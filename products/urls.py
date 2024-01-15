from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.ProductsView.as_view(), name="products"),
    path('single/<int:pk>/', views.ProductView.as_view(), name="single-product"),
    path('list/<int:pk>/', views.ProductsView.as_view(), name="product-detail"),

    path('deliveries/', views.DeliveryView.as_view(), name="deliveries"),
    path('deliveries/<int:pk>/', views.DeliveryView.as_view(), name="edit-delivery"),
    path('delivery/<int:pk>/', views.DeliverySingleView.as_view(), name="view-delivery"),



]

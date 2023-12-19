from . import views
from django.urls import path

urlpatterns = [
    path('details/', views.IncomeExpenseView.as_view(), name="dashboard-details"),
    path('details/products/', views.ProductsView.as_view(), name="dashboard-details")
]

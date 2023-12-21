from . import views
from django.urls import path

urlpatterns = [
    path('details/', views.IncomeExpenseView.as_view(), name="dashboard-details"),
    path('details/products/', views.ProductsView.as_view(), name="dashboard-details"),
    path('transactions/', views.TransactionView.as_view(), name="transaction"),
    path('expense/', views.ExpenseCategoryView.as_view(), name="expense"),
]

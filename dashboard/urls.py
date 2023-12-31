from . import views
from django.urls import path

urlpatterns = [
    path('details/', views.IncomeExpenseView.as_view(), name="dashboard"),
    path('details/products/', views.ProductsView.as_view(), name="dashboard-details"),
    path('transactions/', views.TransactionView.as_view(), name="transaction"),
    path('expense/', views.ExpenseCategoryView.as_view(), name="expense"),
    path('income-expenses/', views.IncomeExpenseDashboardView.as_view(), name="income-expenses"),
]

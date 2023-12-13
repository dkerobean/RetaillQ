from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.SalesView.as_view(), name="sale"),
    path('all/<int:pk>/', views.SalesView.as_view(), name="sale-detail"),
    path('<int:pk>/', views.SaleView.as_view(), name="sale-single"),

    path('expenses/', views.ExpensesView.as_view(), name="expenses"),
    path('expenses/<int:pk>/', views.ExpensesView.as_view(), name="expenses-detail"),
    path('expense/<int:pk>/', views.ExpenseView.as_view(), name="expense-single"),

    path('expenses-category/', views.ExpenseCategoriesView.as_view(), name="expense-category"),
    path('expenses-category/<int:pk>/', views.ExpenseCategoriesView.as_view(), name="expense-detail"),
    path('expense-category/<int:pk>/', views.ExpenseCategoryView.as_view(), name="expense-single"),

    path('transactions/', views.TransactionsView.as_view(), name="transactions"),
    path('transactions/<int:pk>/', views.TransactionsView.as_view(), name="transactions-detail"),
    path('transaction/<int:pk>/', views.TransactionView.as_view(), name="transaction-single"),
]

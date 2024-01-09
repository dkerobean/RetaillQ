from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.SubscriptionView.as_view(), name="all-subscriptions"),
    path('upgrade/', views.UpgradeSubscriptionView.as_view(), name="upgrade-subscription"),
]



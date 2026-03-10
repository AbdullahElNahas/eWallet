from django.urls import path

from . import views

app_name = "Wallets"
urlpatterns = [
    path("create/", views.create_wallet, name="wallet-list-create"),
    path("", views.get_wallet, name="wallet-detail"),
]

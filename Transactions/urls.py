from django.urls import path

from . import views

app_name = "Transactions"
urlpatterns = [
    path("<str:transaction_type>/", views.process_transaction, name="transaction"),
]

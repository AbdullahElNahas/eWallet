from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    recipient = models.ForeignKey(
        "Wallets.Wallet", on_delete=models.CASCADE, related_name="received_transactions"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("10.0"))]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=10, choices=[("deposit", "Deposit"), ("withdrawal", "Withdrawal")]
    )


# Create your models here.

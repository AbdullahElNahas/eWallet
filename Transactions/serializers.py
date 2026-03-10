from decimal import Decimal

from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["recipient", "amount", "timestamp", "type"]
        read_only_fields = ["timestamp", "recipient", "type"]

    def validate_amount(self, value):
        if value < Decimal("10.0"):
            raise serializers.ValidationError("Amount must be at least 10.0")
        return value

    def validate(self, data):
        user = self.context["request"].user
        if not hasattr(user, "wallet"):
            raise serializers.ValidationError("User does not have a wallet")
        return data

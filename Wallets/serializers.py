from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["user", "balance", "created"]
        read_only_fields = ["created", "balance", "user"]

from typing import cast

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Wallets.models import Wallet as WalletModel

from . import serializers


# check if it's withdrawal or deposit from it's pathinfo and then do the transaction accordingly
@api_view(["POST"])
def process_transaction(request, transaction_type):
    if transaction_type not in ["withdrawal", "deposit"]:
        return Response(
            {"error": "Invalid transaction type"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = serializers.TransactionSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        with transaction.atomic():
            lockedWallet = WalletModel.objects.select_for_update().get(
                pk=request.user.wallet.pk
            )

            validatedData = cast(dict, serializer.validated_data)
            amount = validatedData["amount"]
            if transaction_type == "deposit":
                lockedWallet.balance += amount
            else:
                if lockedWallet.balance < amount:
                    return Response(
                        {"error": "Insufficient balance"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                lockedWallet.balance -= amount
            lockedWallet.save()
            serializer.save(recipient=lockedWallet, type=transaction_type)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

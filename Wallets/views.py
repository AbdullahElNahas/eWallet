from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Wallets import serializers


@api_view(["POST"])
def create_wallet(request):
    serializer = serializers.WalletSerializer(data=request.data)
    if serializer.is_valid():
        if hasattr(request.user, "wallet"):
            return Response(
                {"error": "User already has a wallet"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_wallet(request):
    wallet = request.user.wallet
    serializer = serializers.WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_200_OK)

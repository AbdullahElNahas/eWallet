from django.test import TestCase
from rest_framework.test import APIClient


class TransactionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.post(
            "/accounts/register/",
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword123",
            },
            format="json",
        )
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "testpassword123"}
        )
        token = response.data["access"]  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        self.client.post(
            "/wallets/create/",
        )

    def test_deposit_transaction(self):
        # Test creating a transaction with valid data
        response = self.client.post(
            "/transactions/deposit/",
            {"amount": 100.0},
        )
        self.assertEqual(response.status_code, 201)

    def test_create_transaction_invalid_amount(self):
        # Test creating a transaction with an invalid amount
        response = self.client.post(
            "/transactions/withdrawal/",
            {
                "amount": -50.0,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_create_transaction_missing_fields(self):
        # Test creating a transaction with missing required fields
        response = self.client.post(
            "/transactions/deposit/",
            {
                # "amount" is missing
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_withdrawal_transaction(self):
        # First, deposit some money to ensure sufficient balance
        self.client.post(
            "/transactions/deposit/",
            {"amount": 100.0},
        )
        # Test creating a withdrawal transaction with valid data
        response = self.client.post(
            "/transactions/withdrawal/",
            {"amount": 50.0},
        )
        self.assertEqual(response.status_code, 201)

    def test_withdrawal_insufficient_funds(self):
        # Test creating a withdrawal transaction with insufficient funds
        response = self.client.post(
            "/transactions/withdrawal/",
            {"amount": 1000.0},
        )
        self.assertEqual(response.status_code, 400)

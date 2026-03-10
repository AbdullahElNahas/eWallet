from django.test import TestCase
from rest_framework.test import APIClient


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_valid_registration(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_empty_username(self):
        response = self.client.post(
            "/accounts/register/",
            {"username": "", "email": "test1@example.com", "password": ""},
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "testuser2",
                "email": "invalid-email",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email_registration(self):
        self.client.post(
            "/accounts/register/",
            {
                "username": "testuser4",
                "email": "test@example.com",
                "password": "testpassword",
            },
        )
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "testuser1",
                "email": "test@example.com",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_short_password(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "testuser3",
                "email": "test3@example.com",
                "password": "short",
            },
        )
        self.assertEqual(response.status_code, 400)

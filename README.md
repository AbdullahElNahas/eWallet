# eWallet REST API

A production-structured REST API for digital wallet management built with Django REST Framework, PostgreSQL, and Docker.

## Overview

This project implements a backend system for managing digital wallets with full user authentication, wallet creation, and atomic financial transactions. It was built following strict separation of concerns: authentication, wallet state, and transaction logic are each isolated in their own Django app.

## Features

- User registration and JWT authentication (access + refresh tokens)
- Wallet creation with one-to-one user enforcement at the database level
- Deposits and withdrawals with business rule validation (minimum amount, insufficient balance)
- Atomic transactions with row-level locking to prevent race conditions on concurrent balance updates
- Fully containerized with Docker Compose including health-check-based startup ordering
- Automated test suite covering registration, authentication, and transaction business rules

## Tech Stack

- **Backend:** Python, Django 6, Django REST Framework
- **Authentication:** JWT via `djangorestframework-simplejwt`
- **Database:** PostgreSQL 17
- **Containerization:** Docker, Docker Compose
- **Environment Management:** `django-environ`

## Project Structure

```
fDjangoP/
├── accounts/          # User registration and authentication
├── Wallets/           # Wallet model and management
├── Transactions/      # Deposit and withdrawal logic
├── dEwallet/          # Project settings and URL routing
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
└── requirements.txt
```

## Architecture Decisions

**Why three separate apps?**
Each app owns a single responsibility. `accounts` handles identity only. `Wallets` manages wallet state. `Transactions` manages state transitions. This means each can be tested, modified, and reasoned about independently.

**Why `select_for_update()`?**
Without row-level locking, two concurrent withdrawal requests could both read the same balance, both pass the validation check, and both deduct; resulting in a negative balance. `select_for_update()` inside `transaction.atomic()` locks the wallet row until the operation completes, preventing this.

**Why Decimal and not Float?**
Floating point arithmetic is imprecise. Financial systems must use `Decimal` to avoid rounding errors on balance calculations.

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/accounts/register/` | No | Register a new user |
| POST | `/api/token/` | No | Obtain JWT access + refresh tokens |
| POST | `/api/token/refresh/` | No | Refresh access token |
| POST | `/wallets/create/` | Yes | Create wallet for authenticated user |
| GET | `/wallets/` | Yes | Retrieve authenticated user's wallet |
| POST | `/transactions/deposit/` | Yes | Deposit funds into wallet |
| POST | `/transactions/withdrawal/` | Yes | Withdraw funds from wallet |

## Getting Started

### Prerequisites

- Docker and Docker Compose installed

### Run with Docker

```bash
git clone https://github.com/AbdullahElNahas/eWallet.git
cd eWallet
```

Create a `.env` file in the root directory:

```env
DEBUG=TRUE
SECRET_KEY=your-secret-key-here
DB_NAME=ewallet_db
DB_USER=ewallet_owner
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgres://ewallet_owner:your-password@db:5432/ewallet_db
```

Then start the stack:

```bash
docker compose up --build
```

Migrations run automatically on startup. The API will be available at `http://127.0.0.1:8000`.

### Run Tests

```bash
docker exec -it fdjangop-web-1 python manage.py test
```

## Example Usage

**Register a user:**
```json
POST /accounts/register/
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "securepassword123"
}
```

**Get tokens:**
```json
POST /api/token/
{
  "username": "testuser",
  "password": "securepassword123"
}
```

**Deposit funds:**
```json
POST /transactions/deposit/
Authorization: Bearer 
{
  "amount": "100.00"
}
```

## Business Rules

- Minimum transaction amount: 10.00
- Balance cannot go negative
- One wallet per user enforced at database level
- Passwords are hashed and never returned in responses

# 1MeterService API

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0+-blue?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Firebase](https://img.shields.io/badge/Firebase-Realtime_DB-orange?style=flat-square&logo=firebase)

A RESTful API service built with FastAPI for authenticating users and retrieving electricity usage data from Firebase Realtime Database.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Electricity Usage Endpoints](#electricity-usage-endpoints)
  - [Billing and Payment](#billing-and-payment)
  - [Connection Status](#connection-status)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

The 1MeterService API provides a comprehensive backend solution for managing electricity usage data from The IoT device "1Meter". It handles user authentication, storing meter readings, generating usage reports, and billing functionality.

The API connects to a Firebase Realtime Database to store and retrieve electricity usage data, user information, and device connection status.

## ✨ Features

- **User Authentication** - Secure signup and signin functionality
- **Electricity Usage Monitoring** - Track electricity usage at minutely, hourly, daily, and monthly intervals
- **Multiple API Formats** - Both POST (JSON body) and GET (URL parameters) endpoints available
- **Billing System** - Generate and retrieve electricity bills
- **Payment History** - Track payments made by users
- **Device Status Monitoring** - Real-time connection status of devices

## 📚 API Documentation

### Authentication

#### Create User
- **POST** `/auth/signup`
- **Description**: Register a new user with the system
- **Request Body**:
  ```json
  {
    "username": "user123",
    "email": "user@example.com",
    "password": "securepassword",
    "product_id": "meter123"
  }
  ```
- **Response**: 201 Created

#### Login User
- **POST** `/auth/signin`
- **Description**: Authenticate a user
- **Request Body**:
  ```json
  {
    "username": "user123",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "username": "user123",
    "product_id": "meter123"
  }
  ```

### Electricity Usage Endpoints

The API provides several endpoints for retrieving electricity usage data at different time intervals:

#### Minutely Usage
- **POST** `/electricity/minutely`
- **GET** `/electricity/minutely/{product_id}/{date}/{hour}`
- **Description**: Get minute-by-minute electricity usage for a specific hour in a day
- **POST Request Body**:
  ```json
  {
    "product_id": "meter123",
    "date": "2025-03-07",
    "hour": "08"
  }
  ```

#### Hourly Usage
- **POST** `/electricity/hourly`
- **GET** `/electricity/hourly/{product_id}/{date}`
- **Description**: Get hourly electricity usage for a specific day
- **POST Request Body**:
  ```json
  {
    "product_id": "meter123",
    "date": "2025-03-07"
  }
  ```

#### Daily Usage
- **POST** `/electricity/daily`
- **GET** `/electricity/daily/{product_id}/{year_month}`
- **Description**: Get daily electricity usage for a specific month
- **POST Request Body**:
  ```json
  {
    "product_id": "meter123",
    "year_month": "2025-03"
  }
  ```

#### Monthly Usage
- **POST** `/electricity/monthly`
- **GET** `/electricity/monthly/{product_id}/{year}`
- **Description**: Get monthly electricity usage for a specific year
- **POST Request Body**:
  ```json
  {
    "product_id": "meter123",
    "year": "2025"
  }
  ```

### Billing and Payment

#### Get Payment History
- **GET** `/electricity/payments/{username}`
- **Description**: Get the payment history for a user
- **Response**:
  ```json
  {
    "username": "user123",
    "payments": [
      {
        "month": "2025-02",
        "amount": 45.75
      },
      {
        "month": "2025-01",
        "amount": 52.30
      }
    ],
    "email": "user@example.com"
  }
  ```

#### Generate Bill
- **GET** `/electricity/bill/{username}`
- **Description**: Generate a bill for the past month or get an existing paid bill
- **Response**:
  ```json
  {
    "username": "user123",
    "year_month": "2025-02",
    "total_kwh": 320.5,
    "amount": 45.75,
    "is_paid": true,
    "payment_date": "2025-03-05T14:30:00",
    "message": "Bill paid successfully"
  }
  ```

### Connection Status

#### Get All Connection Statuses
- **GET** `/electricity/connection-status`
- **Description**: Get connection status for all users and their products
- **Response**:
  ```json
  {
    "timestamp": "2025-03-07T08:44:21",
    "users": [
      {
        "username": "user123",
        "product_id": "meter123",
        "email": "user@example.com",
        "connection_status": true,
        "last_active": "2025-03-07T08:40:15"
      },
      {
        "username": "user456",
        "product_id": "meter456",
        "email": "user456@example.com",
        "connection_status": false,
        "last_active": "2025-03-06T18:22:33"
      }
    ],
    "total_count": 2
  }
  ```

#### Update Connection Status
- **POST** `/electricity/connection-status`
- **GET** `/electricity/connection-status/{product_id}/{status}`
- **Description**: Update the connection status for a product
- **POST Request Body**:
  ```json
  {
    "product_id": "meter123",
    "status": true
  }
  ```
- **Response**:
  ```json
  {
    "product_id": "meter123",
    "status": true,
    "updated_at": "2025-03-07T08:44:21",
    "message": "Connection status updated successfully"
  }
  ```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Firebase account with Realtime Database set up
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RealChAuLa/1MeterService.git
   cd 1MeterService
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the project root with the following environment variables (or You can add Firebase Admin SDK json to root directory and set `FIREBASE_CREDENTIALS_PATH` in `.env` file): :
   ```
   FIREBASE_API_KEY=your_firebase_api_key
   FIREBASE_AUTH_DOMAIN=your_firebase_auth_domain
   FIREBASE_DATABASE_URL=your_firebase_database_url
   FIREBASE_PROJECT_ID=your_firebase_project_id
   FIREBASE_STORAGE_BUCKET=your_firebase_storage_bucket
   FIREBASE_MESSAGING_SENDER_ID=your_firebase_messaging_sender_id
   FIREBASE_APP_ID=your_firebase_app_id
   
   JWT_SECRET=your_jwt_secret_key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

2. Set up the Firebase Realtime Database rules as needed for your application.

### Running the Application

1. Start the FastAPI server (go to `root` directory or `app` directory):
   ```bash
   python main.py
   ```

2. Access the API documentation at http://localhost:8000/docs or http://localhost:8000/redoc

## 📝 Usage Examples

### Authentication Flow

1. User Registration:
   ```bash
   curl -X POST http://localhost:8000/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"username":"newuser","email":"newuser@example.com","password":"securepass","product_id":"meter789"}'
   ```

2. User Login:
   ```bash
   curl -X POST http://localhost:8000/auth/signin \
     -H "Content-Type: application/json" \
     -d '{"username":"newuser","password":"securepass"}'
   ```

### Get Electricity Usage Data

```bash
# Get hourly data for a specific day
curl -X GET "http://localhost:8000/electricity/hourly/meter123/2025-03-07"

# Get monthly data for 2025
curl -X GET "http://localhost:8000/electricity/monthly/meter123/2025"
```

### Check Connection Status

```bash
# Get all connection statuses
curl -X GET "http://localhost:8000/electricity/connection-status"

# Update connection status
curl -X GET "http://localhost:8000/electricity/connection-status/meter123/true"
```

## 📂 Project Structure

```
1MeterService/
├── app/
│   ├── config.py
│   ├── main.py              # FastAPI application entry point
│   ├── auth/                # Authentication related code
│   │   ├── router.py        # Auth API endpoints
│   │   ├── models.py        # Auth models
│   │   └── service.py       # Auth service
│   ├── electricity/         # Electricity usage related code
│   │   ├── service.py
│   │   ├── router.py        # Electricity API endpoints
│   │   └── models.py        # Electricity data models
│   ├── core/                # Core application modules
│   │   ├── exceptions.py    # Custom exceptions
│   │   ├── security.py      # Security utilities
│   ├── db/                  # Database connections
│   │   └── firebase.py      # Firebase configuration
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
├── main.py                  # Main Appication 
```

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

#### Made with ❤️ by [RealChAuLa](https://github.com/realchaula)
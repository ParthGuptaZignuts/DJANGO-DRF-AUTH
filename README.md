# DJANGO-DRF-AUTH

A simple Django project using Django Rest Framework (DRF) with JWT authentication. This project demonstrates how to set up a Django API with token-based authentication using Simple JWT and handle CORS issues.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [To Integrate Your Gmail Account](#to-integrate-your-gmail-account) 

## Installation

### Prerequisites

Ensure you have Python 3.9 or higher installed. You can download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/). `pip` is usually included with Python.

### Steps to Install

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/ParthGuptaZignuts/DJANGO-DRF-AUTH.git](https://github.com/ParthGuptaZignuts/DJANGO-DRF-AUTH.git)

   cd DJANGO-DRF-AUTH

2. **Set up a virtual environment:**
    ```bash 
    python -m venv venv
    ```

    Activate the virtual environment:
    
    WINDOWS:
    ```bash
    venv\Scripts\activate
    ```

    macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

3. **Install dependencies and get the django setup secret key and paste it into the .env file :**
    ```bash
    pip install -r requirements.txt
    ```
    
    ```bash
    cp env.example .env

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```

4. **Database Migrations:**
    ```bash 
    python manage.py migrate

5. **Run the Server:**
    ```bash
    python manage.py runserver

### API Endpoints
GET /
Simple health check endpoint.

Response:
```json
{
    "message": "Server is working!"
}
```

### TO INTEGRATE YOUR GMAIL ACCOUNT 
Integrating Gmail for Sending Emails
To enable email functionality in this project using Gmail, follow these steps:

Step 1: Enable Less Secure Apps or Use an App Password
Gmail has strict security settings, and by default, it blocks less secure apps.

STEP-1.1 : Generate an App Password

Go to Google App Passwords.
Select "Mail" as the app and "Other (Custom Name)" as the device.
Copy the generated password.

Step 2: Update Your .env File
```bash
"EMAIL_USER" = "your_email"
"EMAIL_PASS" = "password_of_your_email"
"EMAIL_FROM" = "your_email"

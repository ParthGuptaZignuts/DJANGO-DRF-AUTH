# DJANGO-DRF-AUTH

A simple Django project using Django Rest Framework (DRF) with JWT authentication. This project demonstrates how to set up a Django API with token-based authentication using Simple JWT and handle CORS issues.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)

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

    Activate the virtual environment:
    
    WINDOWS:
    venv\Scripts\activate

    macOS/Linux:
    source venv/bin/activate

3. **Install dependencies and get the django setup key and paste it into the .env file :**
    ```bash
    pip install -r requirements.txt
    
    cp env.example .env
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

4. **Database Migrations:**
    ```bash 
    python manage.py migrate

5. **Run the Server:**
    ```bash
    python manage.py runserver

### API Endpoints
GET /api/
Simple health check endpoint.

Response:
```bash
{
  "message": "Server is working!"
}


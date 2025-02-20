# DJANGO-DRF-AUTH

A simple Django project using Django Rest Framework (DRF) with JWT authentication. This project demonstrates how to set up a Django API with token-based authentication using Simple JWT and handle CORS issues.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [API Endpoints](#api-endpoints)
- [To Integrate Your Gmail Account](#to-integrate-your-gmail-account) 
- [Integrating Google Sign-In with Django](#integrating-google-sign-in-with-django)

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
```

### CREATE ADMIN USER
To create an admin user, use the following command:
```bash 
python manage.py create_admin
```

# Integrating Google Sign-In with Django
This guide will walk you through the steps to integrate Google Sign-In functionality into your Django project.

## Step 1: Create a Project in the Google Developer Console

1. **Go to the Google Developer Console:**
   - Open the [Google Cloud Console](https://console.cloud.google.com/).
   - Sign in with your Google account.

2. **Create a New Project:**
   - In the top-left corner, click the **Select a Project** dropdown.
   - Click on **New Project**.
   - Enter a **Project Name** 
   - Click **Create**.

## Step 2: Enable Google+ API (Google OAuth 2.0)

1. **Enable the Google+ API:**
   - In the search bar at the top of the Google Cloud Console, type **Google+ API**.
   - Click on **Google+ API** from the search results.
   - Click **Enable** to enable this API for your project.

## Step 3: Configure OAuth 2.0 Credentials

1. **Go to the Credentials Page:**
   - In the left-hand sidebar, click on **APIs & Services** → **Credentials**.

2. **Create OAuth 2.0 Client ID:**
   - Click the **Create Credentials** button.
   - Select **OAuth 2.0 Client ID** from the dropdown.

3. **Configure OAuth Consent Screen:**
   - If prompted, you'll need to configure the OAuth consent screen.
   - **User Type:** Select **External** and click **Create**.
   - Fill in the required fields such as:
     - **App name:** Enter your app's name.
     - **User support email:** Enter your email.
     - **Developer contact email:** Enter your email.
   - Click **Save and Continue**.

4. **Set Authorized Redirect URIs:**
   - Under the **OAuth 2.0 Client ID** section, in the **Authorized redirect URIs** field, enter your redirect URI:
     - `http://localhost:8000/complete/google/` (for local development).
   - This URL must match the redirect URI in your code.

5. **Save and Obtain Client ID & Client Secret:**
   - After setting up the credentials, you will be presented with your **Client ID** and **Client Secret**.
   - Copy the **Client ID** and **Client Secret** as you will need them for your Django settings.

## Next Steps

### Testing Google Sign-In Integration

To test the Google Sign-In integration, follow these steps:

1. **Construct the Google OAuth2 URL:**
Open your web browser and navigate to the following URL (replace `{your_client_id}` with your actual Google Client ID):

```bash
   https://accounts.google.com/o/oauth2/v2/auth?
     client_id={your_client_id}&
     redirect_uri=http://localhost:8000/complete/google/&
     scope=openid%20email%20profile&
     response_type=code&
     state=random_string
```

2. **Perform Google Login:**
After hitting the URL, you will be redirected to Google's login page.
Log in with your Google account.

3. **Expected Response:**
```json
{
    "success": true,
    "message": "Google login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
}
```
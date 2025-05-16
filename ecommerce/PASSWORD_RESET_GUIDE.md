# Password Reset Functionality Guide

The e-commerce application now includes a complete password reset functionality that allows users to reset their forgotten passwords securely.

## Features

- User-friendly password reset request form
- Secure reset link generation
- Email delivery of reset instructions
- Mobile-responsive design
- Password strength guidelines
- Clear feedback at each step

## How to Test the Password Reset Feature

### 1. Start the Development Server

```bash
cd "c:\Users\Mr. Albert\PyCharmMiscProject\ecommerce"
python manage.py runserver
```

### 2. Access the Password Reset Flow

1. Open your browser and navigate to http://127.0.0.1:8000/login/
2. Click on the "Forgot Password?" link
3. Enter your email address and submit the form
4. You should see the "Password Reset Sent" confirmation page

### 3. Check the Reset Email

Since the application is set to use Django's console email backend in development mode, you won't receive an actual email. Instead, check the terminal where the development server is running to see the password reset email content, including the reset link.

### 4. Follow the Reset Link

Copy the password reset link from the console output and paste it in your browser. You should be taken to the "Set New Password" page.

### 5. Set a New Password

Enter your new password twice and submit the form. If successful, you'll be taken to the "Password Reset Complete" page where you can log in with your new password.

## Production Deployment Notes

For production deployment, the application is configured to use SMTP for sending actual emails. You'll need to configure the following environment variables:

- `EMAIL_HOST`: Your SMTP server (defaults to 'smtp.gmail.com')
- `EMAIL_PORT`: SMTP port (defaults to 587)
- `EMAIL_USE_TLS`: Whether to use TLS (defaults to True)
- `EMAIL_HOST_USER`: SMTP username/email
- `EMAIL_HOST_PASSWORD`: SMTP password
- `DEFAULT_FROM_EMAIL`: The email address used as sender

## Security Features

- One-time use reset links
- Token expiration (links expire after 24 hours)
- Secure token generation
- Password validation rules enforced

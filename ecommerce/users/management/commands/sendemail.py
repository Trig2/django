from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends a test email to verify email configuration is working'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address to send test email to')

    def handle(self, *args, **options):
        recipient = options['email']
        
        self.stdout.write(self.style.WARNING(
            'Attempting to send test email to {}'.format(recipient)
        ))
        
        try:
            # Send test email
            subject = 'Test Email from Django E-commerce App'
            message = 'This is a test email to verify the email functionality is working correctly.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [recipient]
            
            # Print email details for debugging
            self.stdout.write(f"From: {from_email}")
            self.stdout.write(f"To: {recipient}")
            self.stdout.write(f"Subject: {subject}")
            self.stdout.write(f"Message: {message}")
            self.stdout.write(f"Email Backend: {settings.EMAIL_BACKEND}")
            
            # Send the email
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS(
                'Test email sent successfully to {}. Check your console output.'.format(recipient)
            ))
            
            # Instructions for console backend
            if 'console' in settings.EMAIL_BACKEND:
                self.stdout.write(self.style.WARNING(
                    'You are using the console email backend. '
                    'The email should appear above this message in your console.'
                ))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'Failed to send email: {}'.format(str(e))
            ))

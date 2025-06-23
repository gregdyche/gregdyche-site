from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            default=settings.ADMIN_EMAIL,
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        recipient = options['to']
        
        try:
            send_mail(
                subject='Test Email from Django Blog',
                message='This is a test email to verify your email configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Test email sent successfully to {recipient}'
                )
            )
            self.stdout.write(
                f'From: {settings.DEFAULT_FROM_EMAIL}'
            )
            self.stdout.write(
                f'Backend: {settings.EMAIL_BACKEND}'
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'✗ Failed to send test email: {e}'
                )
            )
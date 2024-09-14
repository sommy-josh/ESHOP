# tasks.py

from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_admin_registration_email(username, email):
    send_mail(
        'New User Registration',
        f'New User registered: {username}, email: {email}',
        'chisomzzy1@gmail.com',  # From email
        ['chisomzzy1@gmail.com'],  # Admin email
    )

@shared_task
def send_welcome_email(user_email):
    send_mail(
        'Welcome to our E-commerce platform',
        'Thank you for registering with us!',
        'chisomzzy1@gmail.com',
        [user_email],
    )

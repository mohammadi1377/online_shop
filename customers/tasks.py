from celery import shared_task
from django.core.mail import send_mail
from random import randint
import redis


redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


@shared_task
def send_otp_email(email):
    otp_code = randint(100000, 999999)
    redis_instance.setex(email, 300, otp_code)
    send_mail(
    'Your OTP Code',
    f'Your OTP code is: {otp_code}',
    'noreply@example.com',
    [email],
    fail_silently=False,
    )
from celery import shared_task
from django.core.mail import send_mail
from random import randint
import redis



redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


@shared_task
def send_otp_email(email):
    otp_code = randint(100000, 999999)
    print(otp_code)
    redis_instance.setex(email, 300, otp_code)
    send_mail(
    'Email Verification',
    f'Your OTP code is: {otp_code}',
    'shervinrezaei1378@gmail.com',
    [email],

    )

@shared_task
def send_otp_sms(phone_number):
    otp_code = randint(100000, 999999)
    redis_instance.setex(phone_number, 60, otp_code)




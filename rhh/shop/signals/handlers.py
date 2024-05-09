import random

from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from rhh import settings
from shop.models import UserOtpModel, OrderItem, ProductModel, DjangoUser


@receiver(post_save, sender=DjangoUser)
def send_otp(sender, instance, created, **kwargs):
    if created:
        code = random.randint(100000, 999999)
        UserOtpModel.objects.create(user=instance, code=code)
        send_email(instance.username, code)



def send_email(email, code):
    subject = 'Account Verification'
    message = f'Your Otp is {code}'
    from_email = settings.EMAIL_HOST
    to_email = [email]

    email = EmailMessage(subject, message, from_email, to_email)
    email.send()


@receiver(post_save, sender=OrderItem)
def update_stock(sender, instance, created, **kwargs):
    if created:
        product = ProductModel.objects.filter(id=instance.product.id).get()
        stock = product.product_stock - instance.quantity
        product.product_stock = stock
        product.save()

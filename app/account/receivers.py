import re

from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User


@receiver(pre_save, sender=User)
def lowercase_user_email(instance, **kwargs):
    instance.email = instance.email.lower()


@receiver(pre_save, sender=User)
def fix_user_phone_number(instance, **kwargs):
    if instance.phone is not None:
        instance.phone = re.sub(r'\D', '', instance.phone)

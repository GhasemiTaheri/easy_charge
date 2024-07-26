from celery import shared_task

from .models import Vendor


@shared_task()
def verify_vendor():
    for vendor in Vendor.objects.filter(is_verify=False):
        vendor.is_verify = True
        vendor.save()

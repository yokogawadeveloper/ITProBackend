from django.db.models.signals import post_save
from django.dispatch import receiver
from procurement.models import *
from master.models import *
from approval.models import *


@receiver(post_save, sender=MasterProcurement)
def create_procurement(sender, instance, created, **kwargs):
    if created:
        if instance.RequestType == 'New Hire':
            print('New Hire')
        else:
            print('Replacement')
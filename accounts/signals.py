from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        #add user to group
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        #make user a customer
        Customer.objects.create(user=instance, name=instance.username)
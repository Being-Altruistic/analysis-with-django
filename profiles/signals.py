# Communication System Between Applications
# This signal was built to create a Profile For Every New User

from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# user will send a signal to the profile, whenever a new user is added.
# #OnAction Post-Save
@receiver(post_save, sender=User)
                                    #USer instance
def post_save_create_profile(sender, instance, created, **kwargs):
    # Created is Boolean, not timestamp, True only once.
    if created:
        Profile.objects.create(user=instance)

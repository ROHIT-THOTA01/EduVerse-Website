from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from users.models import Profile

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    # Only save if profile exists to avoid errors
    if hasattr(instance, 'profile'):
        try:
            instance.profile.save()
        except Profile.DoesNotExist:
            # If profile doesn't exist, create it
            Profile.objects.create(user=instance)

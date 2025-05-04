from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import CustomUser, Profile


@receiver(post_save, sender=CustomUser,)
def profile_signal(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk)



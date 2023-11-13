from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        user_profile = Profile.objects.create( # noqa
            user=user,
            display_name=user.organization_name
        )


@receiver(post_save, sender=Profile)
def update_profile(sender, created, instance, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.email = profile.user.email
        user.save()


@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()

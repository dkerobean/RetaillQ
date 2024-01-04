from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CustomUser, Profile, Subscription


@receiver(post_save, sender=CustomUser)
def create_profile_and_subscription(sender, instance, created, **kwargs):
    if created:
        user = instance
        user_profile = Profile.objects.create(
            user=user,
            display_name=user.organization_name
        )

        free_plan_subscription = Subscription.objects.filter(plan='free').first()
        if free_plan_subscription:
            user_profile.subscription = free_plan_subscription
            user_profile.save()
        else:
            free_plan_subscription = Subscription.objects.create(plan='free')


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

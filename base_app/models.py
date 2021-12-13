from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfileModel(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # example of how to add additional fields
    # bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"User Profile for {self.user.username}"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        print("created_running")
        UserProfileModel.objects.create(user=instance)
    instance.userprofilemodel.save()

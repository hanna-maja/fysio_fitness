from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """ A class for holding extra user information """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        """ Return username as default string """
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Signal to create profile when user is create """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ Signal to save profile when user is saved """
    instance.profile.save()

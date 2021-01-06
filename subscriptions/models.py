from django.db import models
import uuid


class SubscriptionPlan(models.Model):
    """ Class to handle subscription plans """
    plan_id = models.CharField(max_length=32, null=False, editable=False)
    name = models.CharField(max_length=254, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    days = models.IntegerField(null=False, blank=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='subscriptions')

    def __str__(self):
        """ Return name of subscription plan as default string """
        return self.name

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the plan id
        if it hasn't been set already.
        """
        if not self.plan_id:
            self.plan_id = uuid.uuid4().hex.upper()
        super().save(*args, **kwargs)

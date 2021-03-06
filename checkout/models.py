import uuid

from django.db import models

from subscriptions.models import SubscriptionPlan


class Order(models.Model):
    """ Class to handle orders """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, 
                                        null=True, blank=True,
                                        related_name='subscription_plans')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        self.order_total = self.subscription_plan.price
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return order_number as default string
        """
        return self.order_number

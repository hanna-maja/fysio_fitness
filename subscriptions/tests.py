from django.test import TestCase
from django.urls import reverse
from .models import SubscriptionPlan
from django.core.files import File


class SubscriptionsIndexViewTests(TestCase):
    def create_plan(self, plan_name, plan_price, days):
        test_image = File(open("static/images/mela1.jpg", 'rb'))
        return SubscriptionPlan.objects.create(name=plan_name, 
            price=plan_price,
            image=test_image,
            days=days,)

    def test_buy_button(self):
        """
        monthly-button should link to checkout
        """
        self.create_plan("test", 100, 30)
        response = self.client.get(reverse('subscriptions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '/checkout?plan_id=1',
            1,
        )
    
    def test_title(self):
        """
        title should be name of plan
        """
        title = "test"
        self.create_plan(title, 100, 30)
        response = self.client.get(reverse('subscriptions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<span class="card-title">{}</span>'.format(title),
            1,
        )

    def test_button_price(self):
        """
        price should be part of buttontext
        """
        price = 199.00
        self.create_plan("test", price, 30)
        response = self.client.get(reverse('subscriptions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="btn" href="/checkout?plan_id=1">Köp {:.2f} kr</a>'.format(price).replace('.',','),
            1,
        )

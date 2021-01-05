from django.test import TestCase
from django.urls import reverse
from django.core.files import File
from subscriptions.models import SubscriptionPlan
from checkout.models import Order
from django.contrib.auth.models import User

class CheckoutViewTests(TestCase):
    def create_plan(self, plan_name, plan_price, days):
        test_image = File(open("static/images/mela1.jpg", 'rb'))
        return SubscriptionPlan.objects.create(name=plan_name, 
            price=plan_price,
            image=test_image)
            
    def test_checkout_price(self):
        """
        Check that price in view is correct
        """
        price = 199.00
        self.create_plan("test", price, 30)
        response = self.client.get(reverse('checkout'),{'plan_id':1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<span>Ditt kort kommer debiteras med <strong>{:.2f} kr</strong></span>'.format(price),
            1,
        )

    def test_post_payment(self):
        """
        Should redirect
        """
        self.create_plan("test", 39, 30)
        data = {
            'plan_id':1,
            'full_name': 'mr cool',
            'email': 'cooling@test.se',
            'phone_number': '784787873787',
            'password': 'asdfasdf',
            'client_secret': 'asdf_secret_1234'
        }
        response = self.client.post(reverse('checkout'),data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('videos'))

    def test_orders_created(self):
        """
        Check that order is created with correct price
        """
        price = 49
        self.create_plan("test", price, 30)
        data = {
            'plan_id':1,
            'full_name': 'mr cool',
            'email': 'cooling@test.se',
            'phone_number': '784787873787',
            'password': 'asdfasdf',
            'client_secret': 'asdf_secret_1234'
        }
        response = self.client.post(reverse('checkout'),data)
        orders = Order.objects.all()
        order = orders[0]
        self.assertEqual(order.order_total, price)


    def test_user_created(self):
        """
        Check that a user is created
        """
        price = 49
        email = 'cooling@test.se'
        self.create_plan("test", price, 30)
        data = {
            'plan_id':1,
            'full_name': 'mr cool',
            'email': email,
            'phone_number': '784787873787',
            'password': 'asdfasdf',
            'client_secret': 'asdf_secret_1234'
        }
        response = self.client.post(reverse('checkout'),data)
        user = User.objects.get(username=email)
        self.assertEqual(user.email, email)

    def test_user_loggedin(self):
        """
        Check that a user is logged in
        """
        price = 49
        email = 'cooling@test.se'
        self.create_plan("test", price, 30)
        data = {
            'plan_id':1,
            'full_name': 'mr cool',
            'email': email,
            'phone_number': '784787873787',
            'password': 'asdfasdf',
            'client_secret': 'asdf_secret_1234'
        }
        response = self.client.post(reverse('checkout'),data)
        self.assertIsNotNone(self.client.session['_auth_user_id'])

    def test_user_exists_should_redirect_to_login(self):
        """
        Check if a user have aa a account and not logged in
        """
        price = 49
        email = 'cooling@test.se'
        self.create_plan("test", price, 30)
        password = 'scjhkdx'
        user = User.objects.create_user(email, email, password)
        data = {
            'plan_id':1,
            'full_name': 'mr cool',
            'email': email,
            'phone_number': '784787873787',
            'password': password,
            'client_secret': 'asdf_secret_1234'
        }
        response = self.client.post(reverse('checkout'),data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('account_login'))

from django.test import TestCase
from django.contrib.auth.models import User
import datetime
from django.urls import reverse

class UserVideoViewTests(TestCase):
    def test_user_not_logged_in(self):
        """
        Check that a user not logged in is redirected
        """
        email = 'cooling@test.se'
        password = 'lhuifwew'
        
        user = User.objects.create_user(email, email, password)
        
        original_date = datetime.date.today() - datetime.timedelta(days=10)
        user.profile.valid_until = original_date
        user.save()

        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 302)
    
    def test_user_valid_until_passed(self):
        """
        Check that a user is valid until date has passed
        """
        email = 'cooling@test.se'
        password = 'lhuifwew'
        
        user = User.objects.create_user(email, email, password)
        
        original_date = datetime.date.today() - datetime.timedelta(days=10)
        user.profile.valid_until = original_date
        user.save()

        self.client.login(username=email, password=password)

        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 302)

    def test_user_valid_until_none(self):
        """
        Check that a user is valid until date is none
        """
        email = 'cooling@test.se'
        password = 'lhuifwew'
        
        user = User.objects.create_user(email, email, password)

        self.client.login(username=email, password=password)

        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 302)

    def test_user_valid_until_works(self):
        """
        Check that a user is valid until date works
        """
        email = 'cooling@test.se'
        password = 'lhuifwew'
        
        user = User.objects.create_user(email, email, password)
        
        original_date = datetime.date.today() + datetime.timedelta(days=10)
        user.profile.valid_until = original_date
        user.save()

        self.client.login(username=email, password=password)

        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 200)

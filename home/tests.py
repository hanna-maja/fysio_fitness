from django.test import TestCase
from django.urls import reverse


class HomeIndexViewTests(TestCase):
    def test_slider_ctabutton(self):
        """
        CTA-button should link to subscription
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="waves-effect waves-light btn-large" href="/traning/">',
        )
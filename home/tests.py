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

    def test_social_buttonfb(self):
        """
        Socialbutton should link to facebook
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'href="https://www.facebook.com/michaela.augustsson.39"',
        )

    def test_social_buttoninsta(self):
        """
        Socialbutton should link to instagram
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'href="https://www.instagram.com/michaelaaugustsson/"',
        )

    def test_social_buttonmail(self):
        """
        Socialbutton should link to mail
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            'href="mailto:fysiofitness007@gmail.com"',
        )
from django.test import TestCase, Client
from django.urls import reverse
from .models import Account

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass',
            'is_reseller': False
        }

    def test_register_view_with_valid_data(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Check that the view redirects
        self.assertRedirects(response, reverse('login'))  # Check that the redirect URL is correct
        self.assertTrue(Account.objects.filter(username='testuser').exists())  # Check that a user was created
        self.assertFalse(Account.objects.filter(user__username='testuser').exists())  # Check that a reseller was not created

    def test_register_view_with_reseller_data(self):
        self.valid_data['is_reseller'] = True
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Check that the view redirects
        self.assertRedirects(response, reverse('login'))  # Check that the redirect URL is correct
        self.assertTrue(Account.objects.filter(username='testuser').exists())  # Check that a user was created
        self.assertTrue(Account.objects.filter(user__username='testuser', is_reseller=True).exists())  # Check that a reseller was created

    def test_register_view_with_invalid_data(self):
        # Submit an empty form to trigger validation errors
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)  # Check that the view returns the form
        self.assertContains(response, 'This field is required.')  # Check that the validation error is displayed

    def test_register_view_with_authenticated_reseller(self):
        # Create a reseller and log in as them
        reseller = Account.objects.create_user(
            username='reseller',
            email='reseller@example.com',
            password='resellerpass',
            is_reseller=True,
        )
        self.client.login(email='reseller@example.com', password='resellerpass')
        # Submit the form with is_reseller=True to create a user under the reseller's account
        self.valid_data['is_reseller'] = True
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Check that the view redirects
        self.assertRedirects(response, reverse('manageUsers'))  # Check that the redirect URL is correct
        self.assertTrue(Account.objects.filter(username='testuser').exists())  # Check that a user was created
        self.assertTrue(Account.objects.filter(user__username='testuser', is_reseller=False, reseller=reseller).exists())  # Check that a user was created under the reseller's account

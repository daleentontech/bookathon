from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_can_create_user_with_email(self):
        """Test creating a new user with email is successful"""
        email = 'test@dprime.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@DPRIME.COM'
        user = get_user_model().objects.create_user(email, 'testpassword')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpassword')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser('test@dprime.com', 'testpassword')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
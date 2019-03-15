from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@fakeemail.com'
        password = 'Testpass098'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@FAKEEMAIL.COM'
        user = get_user_model().objects.create_user(email, 'bleepbloop')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating use with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'bleepbloop')

    def test_create_new_superuser(self):
        """Test creating a new superuser is successful"""
        user = get_user_model().objects.create_superuser(
            'test@fakeemail.com',
            'bleepbloop123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
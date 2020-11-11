from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_successful_minimum_requirements(self):
        """
        Test creating a new custom User with username
        and password successfully
        """
        username = 'usernametest'
        password = 'testpassword'

        user = get_user_model().objects.create_user(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_complete_user_successful(self):
        """Test creating a new custom User"""
        username = 'usernametest'
        age = 22
        biography = 'This is my biography aaaaaaaaaaaaaah'
        password = 'testpassword'

        user = get_user_model().objects.create_user(
            username=username,
            age=age,
            biography=biography,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.age, age)
        self.assertEqual(user.biography, biography)
        self.assertTrue(user.check_password(password))

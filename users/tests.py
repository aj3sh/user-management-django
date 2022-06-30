from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class UserModelTests(TestCase):

    def test_user_create(self):
        # testing new user and its data
        user = User.objects.create_user(email='aj3sshh@gmail.com', password='myPassword')
        self.assertFalse(str(user.pk).isdigit()) # testing if user's pk is not integer value
        self.assertEqual(user.email, 'aj3sshh@gmail.com')
        self.assertEqual(user.get_username(), user.email)
        self.assertTrue(user.check_password('myPassword'))
        with self.assertRaises(AttributeError):
            # username does not exists in our model
            user.username

        # testing user creation error
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="myPassword")

        # testing super user
        superuser = User.objects.create_superuser(email='superuser@gmail.com', password='myPassword')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff) # testing if is_staff is True (used for Django Admin)
        self.assertTrue(superuser.is_superuser)
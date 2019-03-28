from django.test import TestCase
from django.test import Client
from django.core.exceptions import ValidationError

from Hasker.profile.models import HaskerUser


class TestProfileModel(TestCase):

    def test_hasker_user_model_with_correct_values(self):
        username = "test"
        email = "email@email.ru"
        password = "123"

        new_user = HaskerUser(username=username, email=email)
        new_user.set_password(password)
        new_user.save()

        user = HaskerUser.objects.get(username=username)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)

        c = Client()
        self.assertTrue(c.login(username=username, password=password))

    def test_hasker_user_model_with_incorrect_values(self):
        username = "user"*100
        password = "123"*100
        email = "email"

        new_user = HaskerUser(username=username, email=email, password=password)
        self.assertRaises(ValidationError, new_user.full_clean)

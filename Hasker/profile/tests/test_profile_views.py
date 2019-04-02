from django.test import TestCase
from django.test import Client
from django.urls import reverse

from Hasker.httpcodes import HTTP_FOUND, HTTP_OK, HTTP_UNAUTHORIZED, HTTP_BAD_REQUEST
from Hasker.profile.models import HaskerUser


class TestProfileViews(TestCase):
    username = 'test1'
    password = '123'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user1 = HaskerUser(username=cls.username, email="email@email.ru")
        user1.set_password(cls.password)
        user1.save()

    def test_login_view_with_correct_credentials(self):
        c = Client()
        response = c.post(reverse('login'), {'login': self.username, 'password': self.password}, follow=True)
        path, code = response.redirect_chain[0]

        self.assertEqual(path, '/')
        self.assertEqual(code, HTTP_FOUND)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_login_view_with_incorrect_credentials(self):
        c = Client()
        response = c.post(reverse('login'), {'login': 'xxx', 'password': 'xxx'}, follow=True)

        self.assertEqual(response.status_code, HTTP_UNAUTHORIZED)

    def test_logout_view(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('logout'), follow=True)
        path, code = response.redirect_chain[0]

        self.assertEqual(path, '/')
        self.assertEqual(code, HTTP_FOUND)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_signup_view_with_correct_values(self):
        username = "new_user"
        password = "12345678"
        email = "test@gmail.com"

        c = Client()
        response = c.post(reverse('signup'), {'username': username, 'email': email,
                                              'password': password, 'password_again': password})
        self.assertEqual(response.status_code, HTTP_OK)
        login_result = c.login(username=username, password=password)
        self.assertTrue(login_result)

    def test_signup_view_with_incorrect_values(self):
        username = "user" * 100
        password = "123" * 100
        email = "email"

        c = Client()
        response = c.post(reverse('signup'), {'username': username, 'email': email,
                                              'password': password, 'password_again': password})
        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)

    def test_settings_view_with_correct_values(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        new_email = "xxx@xxx.ru"
        new_password = "456456456456"

        response = c.post(reverse('settings'), {'email': new_email, 'password': new_password,
                                                'password_again': new_password})
        self.assertEqual(response.status_code, HTTP_OK)

        c.logout()
        self.assertTrue(c.login(username=self.username, password=new_password))
        # check email in DB
        user = HaskerUser.objects.get(username=self.username)
        self.assertEqual(user.email, new_email)

    def test_settings_view_with_incorrect_values(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        new_email = "email"
        new_password = "123" * 100

        response = c.post(reverse('settings'), {'email': new_email, 'password': new_password,
                                                'password_again': new_password})
        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)

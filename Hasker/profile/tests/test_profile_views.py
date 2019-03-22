from django.test import TestCase
from django.test import Client
from Hasker.httpcodes import *
from Hasker.profile.models import HaskerUser
from django.contrib.auth import get_user_model
# HaskerUser = get_user_model()


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
        response = c.post('/login/', {'login': self.username, 'password': self.password}, follow=True)
        path, code = response.redirect_chain[0]

        self.assertEqual(path, '/')
        self.assertEqual(code, HTTP_FOUND)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_login_view_with_incorrect_credentials(self):
        c = Client()
        response = c.post('/login/', {'login': 'xxx', 'password': 'xxx'}, follow=True)

        self.assertEqual(response.status_code, HTTP_UNAUTHORIZED)

    def test_logout_view(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.get('/logout/', follow=True)
        path, code = response.redirect_chain[0]

        self.assertEqual(path, '/')
        self.assertEqual(code, HTTP_FOUND)
        self.assertEqual(response.status_code, HTTP_OK)

    def test_signup_view_with_correct_values(self):
        username = "new_user"
        password = "123456"
        email = "test@gmail.com"

        c = Client()
        response = c.post('/signup/', {'username': username,
                                       'email': email,
                                       'password': password,
                                       'password_again': password})
        self.assertEqual(response.status_code, HTTP_OK)
        login_result = c.login(username=username, password=password)
        self.assertTrue(login_result)

    def test_signup_view_with_incorrect_values(self):
        username = "user"*100
        password = "123"*100
        email = "email"

        c = Client()
        response = c.post('/signup/', {'username': username,
                                       'email': email,
                                       'password': password,
                                       'password_again': password})
        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)
        #
        # self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        # self.assertFormError(response, 'form', 'username',
        #                      'Ensure this value has at most 150 characters (it has 400).')
        # self.assertFormError(response, 'form', 'password',
        #                      'Ensure this value has at most 128 characters (it has 300).')

    def test_settings_view_with_correct_values(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        new_email = "xxx@xxx.ru"
        new_password = "456"

        response = c.post('/settings/', {'email': new_email,
                                         'password': new_password,
                                         'password_again': new_password })
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
        new_password = "123"*100

        response = c.post('/settings/', {'email': new_email,
                                         'password': new_password,
                                         'password_again': new_password})
        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)

        # self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')
        # self.assertFormError(response, 'form', 'password',
        #                      'Ensure this value has at most 128 characters (it has 300).')

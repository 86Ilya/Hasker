import json

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from Hasker.profile.models import HaskerUser


class AuthTests(APITestCase):
    # TODO make it work!
    # url = reverse('api_profile')
    url = '/api/v1/auth/'

    def setUp(self):
        self.test_user = HaskerUser(username='test_user', email='email@email.ru')
        self.test_user.set_password('test_password')
        self.test_user.save()
        self.test_user_token = Token.objects.get_or_create(user=self.test_user)

    def test_auth(self):
        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content.decode())['token']
        self.assertEqual(token, self.test_user_token[0].key)

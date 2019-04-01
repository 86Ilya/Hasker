import json

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from Hasker.profile.models import HaskerUser


class AuthTests(APITestCase):
    # TODO make it work!
    # url = reverse('api_profile')
    url = '/api/v1/auth/'

    def test_auth(self):
        test_user = HaskerUser(username='test_user', email='email@email.ru')
        test_user.set_password('test_password')
        test_user.save()
        test_user_token = Token.objects.get_or_create(user=test_user)

        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = json.loads(response.content.decode())['token']
        self.assertEqual(token, test_user_token[0].key)

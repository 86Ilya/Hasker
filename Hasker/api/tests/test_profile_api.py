import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from Hasker.profile.models import HaskerUser


class ProfileTests(APITestCase):
    # urlpatterns = [
    #     path('', include(api_url_patterns)),
    # ]
    # TODO make it work!
    # url = reverse('api_profile')
    url = '/api/v1/profile/'

    # READ - GET
    def test_get_user_info(self):
        client = APIClient()

        test_user = HaskerUser(username='test_user1', email='emai1@email.ru')
        test_user.set_password('test_password')
        test_user.save()
        test_user_token = Token.objects.get_or_create(user=test_user)

        client.credentials(HTTP_AUTHORIZATION='Token ' + test_user_token[0].key)
        response = client.get(self.url, {}, format='json')
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['username'], 'test_user1')
        print(response.content)

    # CREATE - POST
    def test_create_account_with_correct_values(self):
        data = {'username': 'new_hasker_user1', 'email': 'ddd@am.ru',
                'password': '12345678', 'password_again': '12345678'}
        client = APIClient()
        response = client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HaskerUser.objects.get(username='new_hasker_user1'))

    def test_create_account_with_incorrect_values(self):
        client = APIClient()
        data = {'username': 'new_hasker_user2', 'email': 'dddam.ru',
                'password': '1', 'password_again': '1'}
        response = client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(HaskerUser.objects.filter(username='hasker_new_user2')), 0)

    def test_create_account_when_username_exists(self):
        client = APIClient()
        data = {'username': 'test_user4', 'email': 'ddd@am.ru',
                'password': '12345678', 'password_again': '12345678'}

        test_user = HaskerUser(username='test_user4', email='emai1@email.ru')
        test_user.set_password('test_password')
        test_user.save()

        response = client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # UPDATE - PUT
    def test_update_existed_account(self):
        client = APIClient()
        data = {'username': 'test_user5', 'email': 'new_email@x.ru', 'password': '12345678',
                'password_again': '12345678'}

        test_user = HaskerUser(username='test_user5', email='emai1@email.ru')
        test_user.set_password('test_password')
        test_user.save()
        test_user_token = Token.objects.get_or_create(user=test_user)

        client.credentials(HTTP_AUTHORIZATION='Token ' + test_user_token[0].key)
        response = client.put(self.url, data, format='json')
        content = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['email'], 'new_email@x.ru')

    # DELETE - DELETE
    def test_delete_existed_account(self):
        client = APIClient()
        test_user_for_del = HaskerUser(username='test_user_for_del', email='email_user_for_del@email.ru',
                                       password='no matter...')
        test_user_for_del.save()
        test_user_token = Token.objects.get_or_create(user=test_user_for_del)

        # check user exists in db
        self.assertTrue(HaskerUser.objects.get(username='test_user_for_del'))
        client.credentials(HTTP_AUTHORIZATION='Token ' + test_user_token[0].key)
        response = client.delete(self.url, {}, format='json')
        # check user exists in db
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(HaskerUser.objects.filter(username='test_user_for_del')), 0)

import base64

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from Hasker.profile.forms import HaskerUserSettingsForm, HaskerUserForm


class TestProfileForms(TestCase):
    avatar_image_encoded = b'/9j/4AAQSkZJRgABAQEASABIAAD/2wCEAP//////////////////////////////////////////////////////' \
                           b'//////////////////////////////8B////////////////////////////////////////////////////////' \
                           b'///////////////////////////////CABEIAAEAAQMBEQACEQEDEQH/xAAUAAEAAAAAAAAAAAAAAAAAAAAD/9oA' \
                           b'CAEBAAAAAE//xAAUAQEAAAAAAAAAAAAAAAAAAAAA/9oACAECEAAAAH//xAAUAQEAAAAAAAAAAAAAAAAAAAAA/9oA' \
                           b'CAEDEAAAAH//xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oACAEBAAE/AH//xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oA' \
                           b'CAECAQE/AH//xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oACAEDAQE/AH//2Q==i'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_hasker_user_form_with_correct_values(self):
        username = 'test'
        password = '12346578'
        email = 'email@email.ru'
        avatar = {'avatar': SimpleUploadedFile('avatar.jpeg', base64.decodebytes(self.avatar_image_encoded))}
        form_data = {
            'username': username,
            'password': password,
            'password_again': password,
            'email': email,
            'avatar': avatar
        }

        form = HaskerUserForm(form_data, avatar)
        self.assertTrue(form.is_valid())

    def test_hasker_user_form_with_incorrect_values(self):
        username = "user" * 100
        password = "123" * 100
        email = "email"
        avatar = {'avatar': SimpleUploadedFile('avatar.jpeg', b'xxx')}

        form_data = {
            'username': username,
            'password': password,
            'password_again': password,
            'email': email,
            'avatar': avatar
        }

        form = HaskerUserForm(form_data, avatar)
        self.assertFalse(form.is_valid())
        # TODO how to do this right?
        self.assertEqual(form.errors['username'][0], 'Ensure this value has at most 150 characters (it has 400).')
        self.assertEqual(form.errors['email'][0], 'Enter a valid email address.')
        self.assertEqual(form.errors['password'][0], 'Ensure this value has at most 128 characters (it has 300).')
        self.assertEqual(form.errors['avatar'][0],
                         'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')

    def test_hasker_user_settings_form_with_correct_values(self):
        username = 'test'
        password = '12345678'
        email = 'email@email.ru'
        avatar = {'avatar': SimpleUploadedFile('avatar.jpeg', base64.decodebytes(self.avatar_image_encoded))}
        form_data = {
            'username': username,
            'password': password,
            'password_again': password,
            'email': email,
            'avatar': avatar
        }

        form = HaskerUserSettingsForm(form_data, avatar)
        self.assertTrue(form.is_valid())

    def test_hasker_user_settings_form_with_incorrect_values(self):
        username = "user"
        password = "123" * 100
        email = "email"
        avatar = {'avatar': SimpleUploadedFile('avatar.jpeg', b'xxx')}

        form_data = {
            'username': username,
            'password': password,
            'password_again': password,
            'email': email,
            'avatar': avatar
        }

        form = HaskerUserSettingsForm(form_data, avatar)
        self.assertFalse(form.is_valid())
        # TODO how to do this right?
        self.assertEqual(form.errors['email'][0], 'Enter a valid email address.')
        self.assertEqual(form.errors['password'][0], 'Ensure this value has at most 128 characters (it has 300).')
        self.assertEqual(form.errors['avatar'][0],
                         'Upload a valid image. The file you uploaded was either not an image or a corrupted image.')

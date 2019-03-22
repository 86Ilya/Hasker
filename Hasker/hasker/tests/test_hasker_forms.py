from django.test import TestCase
from Hasker.hasker.forms import AnswerForm, AskForm


class TestHaskerForms(TestCase):

    def test_ask_form_with_correct_values(self):
        header = 'ask form'
        content = 'content'
        tags = ['1', '2', '3']

        form_data = {
            'header': header,
            'content': content,
            'tags': tags,
        }

        form = AskForm(form_data)
        self.assertTrue(form.is_valid())

    def test_ask_form_with_incorrect_values(self):
        header = 'a' * 257
        content = 'c' * 1025
        tags = ['x']

        form_data = {
            'header': header,
            'content': content,
            'tags': tags,
        }

        form = AskForm(form_data)
        self.assertFalse(form.is_valid())
        # TODO how to do this right?
        self.assertEqual(form.errors['header'][0], 'Ensure this value has at most 256 characters (it has 257).')
        self.assertEqual(form.errors['content'][0], 'Ensure this value has at most 1024 characters (it has 1025).')
        self.assertEqual(form.errors['tags'][0], 'Select a valid choice. x is not one of the available choices.')

    def test_answer_form_with_correct_values(self):
        content = 'answer content'

        form_data = {
            'content': content,
        }

        form = AnswerForm(form_data)
        self.assertTrue(form.is_valid())

    def test_answer_form_with_incorrect_values(self):
        content = 't'*1025

        form_data = {
            'content': content,
        }

        form = AnswerForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'][0], 'Ensure this value has at most 1024 characters (it has 1025).')

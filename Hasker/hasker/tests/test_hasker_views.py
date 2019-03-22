from django.test import TestCase
from django.test import Client

from Hasker.hasker.models import Question, Answer, Tag
from Hasker.profile.models import HaskerUser
from Hasker.httpcodes import *


class TestHaskerViews(TestCase):
    username1 = "test1"
    username2 = "test2"

    password1 = "123"
    password2 = "456"

    email = "email@email.ru"
    # see hasker.forms 'if DEBUG:..'
    tag_names_list = ['c++', 'scala', 'python', 'java', 'javascript', 'django', 'css']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user1 = HaskerUser(username=cls.username1, email=cls.email)
        user1.set_password(cls.password1)
        user1.save()

        user2 = HaskerUser(username=cls.username2, email=cls.email)
        user2.set_password(cls.password2)
        user2.save()

        # create tags
        tag_names_list = ['c++', 'scala', 'python', 'java', 'javascript', 'django', 'css']
        for tag in tag_names_list:
            Tag(tag_name=tag).save()

        # create question
        for i in range(3):
            question = Question(header="question"+str(i), content="abc"*64, author=user1)
            question.save()

            # add tag
            tag = Tag.objects.get(tag_name=cls.tag_names_list[i])
            question.tags.add(tag)
            # create answer
            answer = Answer(content="zxc"*64, author=user2, question=question)
            answer.save()
            answer.likes.add(user2)
            answer.save()

            question.save()

    def test_main_view(self):
        c = Client()
        response = c.get('/')

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, "question0", 2, HTTP_OK)
        self.assertContains(response, "question1", 2, HTTP_OK)
        self.assertContains(response, "question2", 2, HTTP_OK)

    def test_search_view_with_correct_values(self):
        c = Client()
        response = c.get('/search/question0/')

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, "question0", 2, HTTP_OK)
        self.assertContains(response, "question1", 1, HTTP_OK)
        self.assertContains(response, "question2", 1, HTTP_OK)

    def test_search_view_with_incorrect_values(self):
        c = Client()
        response = c.get('/search/{}/'.format('a'*1025))
        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)

    def test_search_by_tag_view_with_correct_values(self):
        c = Client()
        response = c.get('/tag/c++/')

        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, "question0", 2, HTTP_OK)
        self.assertContains(response, "question1", 1, HTTP_OK)
        self.assertContains(response, "question2", 1, HTTP_OK)

    def test_search_by_tag_view_with_incorrect_values(self):
        c = Client()
        response = c.get('/tag/caramba/')
        self.assertEqual(response.status_code, HTTP_NOT_FOUND)

    def test_ask_view_with_correct_values(self):
        c = Client()
        c.login(username=self.username1, password=self.password1)
        ask_question_data = {
            'header': 'new question',
            'content': 'new content',
            'tags': ['1', '2', '3']
        }
        response = c.post('/ask/', ask_question_data, follow=True)
        path, code = response.redirect_chain[0]

        self.assertRegex(path, r'/question\d*')
        self.assertEqual(code, HTTP_FOUND)
        self.assertEqual(response.status_code, HTTP_OK)

        question_from_db = Question.objects.get(header="new question")
        tags = question_from_db.get_tags()
        self.assertEqual(tags[0]['tag_name'], self.tag_names_list[0])
        self.assertEqual(tags[1]['tag_name'], self.tag_names_list[1])
        self.assertEqual(tags[2]['tag_name'], self.tag_names_list[2])

        self.assertEquals(question_from_db.author.username, self.username1)

    def test_ask_view_with_incorrect_values(self):
        c = Client()
        c.login(username=self.username1, password=self.password1)
        ask_question_data = {
            'header': 'n'*1025,
            'content': 't'*1025,
        }
        response = c.post('/ask/', ask_question_data, follow=True)

        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)

    def test_question_view(self):
        header = 'testing question view'
        content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        question = Question(header=header, content=content, author=user)
        question.save()

        response = c.get('/question{}/?page=1'.format(question.id))
        self.assertContains(response, header, 2, HTTP_OK)
        self.assertContains(response, content, 1, HTTP_OK)

    def test_question_view_add_correct_answer(self):
        header = 'testing question view add correct answer'
        content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        question = Question(header=header, content=content, author=user)
        question.save()

        c.login(username=self.username1, password=self.password1)
        answer_data = {'content': 'z'*100}
        response = c.post('/question{}/'.format(question.id), answer_data, follow=True)
        answer_from_db = Answer.objects.get(content=answer_data['content'])

        path, code = response.redirect_chain[0]
        self.assertEqual(path, r'/question{}/?page=1#answer{}'.format(question.id, answer_from_db.id))
        self.assertEqual(code, HTTP_FOUND)
        self.assertEqual(response.status_code, HTTP_OK)
        self.assertContains(response, answer_data['content'], 1, HTTP_OK)

    def test_question_view_add_incorrect_answer(self):
        header = 'testing question view add incorrect answer'
        question_content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        question = Question(header=header, content=question_content, author=user)
        question.save()

        c.login(username=self.username1, password=self.password1)
        answer_data = {'content': 'z'*1025}
        response = c.post('/question{}/'.format(question.id), answer_data, follow=True)
        self.assertEqual(response.status_code, HTTP_BAD_REQUEST)

        answer_from_db = Answer.objects.filter(content=answer_data['content'])
        # TODO is this right?
        self.assertEqual(len(answer_from_db), 0)

    def test_question_vote(self):
        header = 'testing question vote'
        question_content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        user2 = HaskerUser.objects.get(username=self.username2)

        question = Question(header=header, content=question_content, author=user)
        question.save()

        c.login(username=self.username2, password=self.password2)
        response = c.post('/question{}/like'.format(question.id), {})
        self.assertJSONEqual(response.content.decode(), {"rating": 1, "result": True})
        self.assertEqual(question.likes.values()[0]['username'], user2.username)

    def test_answer_add_like(self):
        question_header = 'testing answer like'
        question_content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        user2 = HaskerUser.objects.get(username=self.username2)

        question = Question(header=question_header, content=question_content, author=user)
        question.save()

        answer = Answer(content="a"*10, author=user, question=question)
        answer.save()

        c.login(username=self.username2, password=self.password2)
        response = c.post('/answer{}/like'.format(answer.id))
        self.assertJSONEqual(response.content.decode(), {"rating": 1, "result": True})
        self.assertEqual(answer.likes.values()[0]['username'], user2.username)

    def test_answer_add_dislike(self):
        question_header = 'testing answer dislike'
        question_content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        user2 = HaskerUser.objects.get(username=self.username2)

        question = Question(header=question_header, content=question_content, author=user)
        question.save()

        answer = Answer(content="a"*10, author=user, question=question)
        answer.save()

        c.login(username=self.username2, password=self.password2)
        response = c.post('/answer{}/dislike'.format(answer.id))
        self.assertJSONEqual(response.content.decode(), {"rating": -1, "result": True})
        self.assertEqual(answer.dislikes.values()[0]['username'], user2.username)

    def test_answer_add_star(self):
        question_header = 'testing answer star'
        question_content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        user2 = HaskerUser.objects.get(username=self.username2)

        question = Question(header=question_header, content=question_content, author=user)
        question.save()

        answer = Answer(content="a"*10, author=user2, question=question)
        answer.save()

        c.login(username=self.username1, password=self.password1)
        self.assertFalse(answer.correct)
        response = c.post('/answer{}/add_star'.format(answer.id))
        self.assertJSONEqual(response.content.decode(), {"correct": True, "result": True})
        answer_from_db = Answer.objects.get(id=answer.id)
        self.assertTrue(answer_from_db.correct)

    def test_answer_remove_star(self):
        question_header = 'testing answer remove star'
        question_content = 'a'*100
        c = Client()
        user = HaskerUser.objects.get(username=self.username1)
        user2 = HaskerUser.objects.get(username=self.username2)

        question = Question(header=question_header, content=question_content, author=user)
        question.save()

        answer = Answer(content="a"*10, author=user2, question=question)
        answer.save()

        c.login(username=self.username1, password=self.password1)
        response = c.post('/answer{}/add_star'.format(answer.id))
        self.assertJSONEqual(response.content.decode(), {"correct": True, "result": True})

        response = c.post('/answer{}/remove_star'.format(answer.id))
        self.assertJSONEqual(response.content.decode(), {"correct": False, "result": True})

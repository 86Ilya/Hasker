import random
import json
from loremipsum import get_paragraph, get_sentence
from collections import namedtuple

from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from Hasker.profile.models import HaskerUser
from Hasker.hasker.models import Question, Answer, Tag

QuestionTuple = namedtuple("QuestionTuple", "id header tags content author")


class HaskerTests(APITestCase):

    def setUp(self):
        """ Create questions and answers """

        self.questions = """What is my ip?
                            What time is it?
                            How to register to vote?
                            How to tie a tie?
                            Can you run it?
                            What song is this?"""

        users_list = list()
        for i in range(10):
            user = HaskerUser(username="iam_test{}".format(i), email="email@email{}.ru".format(i))
            user.set_password('1')
            user.save()
            users_list.append(user)

        # create tags
        tags_list = list()
        tag_names_list = ['c++', 'scala', 'python', 'java', 'javascript', 'django', 'css']
        for tag_name in tag_names_list:
            tag = Tag(tag_name=tag_name)
            tag.save()
            tags_list.append(tag)

        # create questions
        self.questions_list = list()
        for line in self.questions.split('\n'):
            question = Question(header=line.strip(),
                                content=get_paragraph()[:1000],
                                author=random.choice(users_list))
            question.save()
            question.tags.add(random.choice(tags_list))
            question.save()

            question_tuple = QuestionTuple(question.id,
                                           question.header,
                                           question.get_tags(),
                                           question.content,
                                           question.author.username)
            self.questions_list.append(question_tuple)

            # create answers
            for j in range(random.randint(10, 40)):
                answer_content = get_sentence()
                answer = Answer(content=answer_content, author=random.choice(users_list), question=question)
                answer.save()

        self.token = Token.objects.get_or_create(user=users_list[0])[0].key

    def test_index_page(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse('questions_index')
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content), len(self.questions.split('\n')))

    def test_search_question_by_content(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        question = random.choice(self.questions_list)
        url = reverse('questions_search', args=[question.content])
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['header'], question.header)
        self.assertEqual(content[0]['content'], question.content)
        self.assertEqual(content[0]['author'], question.author)
        self.assertDictEqual(content[0]['tags'][0], question.tags[0])

    def test_search_question_by_header(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        question = random.choice(self.questions_list)
        url = reverse('questions_search', args=[question.header])
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode())
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['header'], question.header)
        self.assertEqual(content[0]['content'], question.content)
        self.assertEqual(content[0]['author'], question.author)
        self.assertDictEqual(content[0]['tags'][0], question.tags[0])

    def test_get_question_by_id(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        question = random.choice(self.questions_list)
        url = reverse('question_by_id', args=[question.id])
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode())
        self.assertEqual(content['header'], question.header)
        self.assertEqual(content['content'], question.content)

    def test_get_question_answers(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        question = random.choice(self.questions_list)
        question_from_db = Question.objects.get(id=question.id)
        answers_from_db = Answer.objects.filter(question=question_from_db)
        url = reverse('answers', args=[question.id])
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content.decode())
        self.assertEqual(len(answers_from_db), len(content))

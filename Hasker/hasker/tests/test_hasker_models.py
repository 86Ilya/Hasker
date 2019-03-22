from django.test import TestCase
from django.core.exceptions import ValidationError
from Hasker.hasker.models import Question, Answer, Tag
from Hasker.profile.models import HaskerUser


class TestHaskerModels(TestCase):


    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # create users
        user1 = HaskerUser(username="test1", email="email@email.ru", password="123")
        user1.save()
        user2 = HaskerUser(username="test2", email="email2@email.ru", password="321")
        user2.save()
        user3 = HaskerUser(username="test3", email="email3@email.ru", password="456")
        user3.save()

        # create tags
        # tag_names_list = ['c++', 'scala', 'python', 'java', 'javascript', 'django', 'css']
        # for tag in tag_names_list:
        #     Tag(tag_name=tag).save()

        # create question
        question = Question(header="main question", content="abc"*64, author=user1)
        question.save()
        # for i in range(3):
        #     question.tags.add(Tag.objects.get(tag_name=tag_names_list[i]))
        # question.save()

        # create answers
        answer1 = Answer(content="zxc"*64, author=user2, question=question)
        answer1.save()
        answer1.likes.add(user2)
        answer1.save()

    def test_question_with_correct_values(self):
        header = 'question header'
        content = 'content'
        user1 = HaskerUser.objects.get(username="test1")
        question = Question(header=header, content=content, author=user1)
        question.save()

        question_from_db = Question.objects.get(author=user1, header=header)
        self.assertEquals(question_from_db.header, header)
        self.assertEquals(question_from_db.content, content)

    def test_question_with_incorrect_values(self):
        header = 'q'*257
        content = 'c'*1025
        user1 = HaskerUser.objects.get(username="test1")
        question = Question(header=header, content=content, author=user1)
        self.assertRaises(ValidationError, question.full_clean)

        question_from_db = Question.objects.filter(author=user1, header=header)
        # TODO how to do this right?
        self.assertEquals(len(question_from_db), 0)

    def test_answer_with_correct_values(self):
        user1 = HaskerUser.objects.get(username="test1")
        content = "content"
        question = Question.objects.get(header="main question")

        answer = Answer(content=content, author=user1, question=question)
        answer.save()

        answer_from_db = Answer.objects.get(content=content)
        self.assertEqual(answer_from_db.author, user1)

    def test_answer_with_incorrect_values(self):
        user1 = HaskerUser.objects.get(username="test1")
        content = "c"*1025
        question = Question.objects.get(header="main question")

        answer = Answer(content=content, author=user1, question=question)
        self.assertRaises(ValidationError, answer.full_clean)

        answer_from_db = Answer.objects.filter(content=content)
        # TODO how to do this right?
        self.assertEquals(len(answer_from_db), 0)

    def test_like_exists(self):
        user1 = HaskerUser.objects.get(username="test1")

        question = Question.objects.get(header="main question")
        question.likes.add(user1)
        question.save()
        # TODO likes=user1?
        question_from_db = Question.objects.get(likes=user1)
        self.assertEqual(question_from_db.header, "main question")


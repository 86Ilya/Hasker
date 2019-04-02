from django.db.models import Q

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from Hasker.hasker.models import Question, Answer
from Hasker.api.serializers import QuestionSerializer, AnswerSerializer
from Hasker.settings import QUESTIONS_PER_PAGE, ANSWERS_PER_PAGE


class QuestionListView(generics.ListAPIView):
    """
    get:
    Return list of all questions
    """
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    paginate_by = QUESTIONS_PER_PAGE
    queryset = Question.objects.all()


class QuestionTrendingListView(generics.ListAPIView):
    """
    get:
    Return list of trending questions
    """
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    paginate_by = QUESTIONS_PER_PAGE
    queryset = Question.objects.all().order_by('likes', '-dislikes')


class QuestionSearchListView(generics.ListAPIView):
    """
    get:
    Return list of questions by pattern
    """
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    paginate_by = QUESTIONS_PER_PAGE

    def get_queryset(self):
        query = self.kwargs.get('query', None)
        if query:
            queryset = Question.objects.filter(Q(content__contains=query) | Q(header__contains=query))
        else:
            queryset = Question.objects.all()
        return queryset


class QuestionByIDView(generics.RetrieveAPIView):
    """
    get:
    Return question by id
    """
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = 'id'
    queryset = Question.objects.all()


class AnswersListView(generics.ListAPIView):
    """
    get:
    Return list of answers by questin id
    """
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    paginate_by = ANSWERS_PER_PAGE

    def get_queryset(self):
        question_id = self.kwargs.get('id', None)
        if question_id:
            question = Question.objects.get(id=question_id)
            queryset = Answer.objects.filter(question=question)
        else:
            queryset = Answer.objects.all()
        return queryset

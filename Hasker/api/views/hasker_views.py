from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from Hasker.hasker.models import Question
from Hasker.api.serializers import QuestionSerializer
from Hasker.api.views.base_manage_view import BaseManageView


class QuestionCreateView(generics.CreateAPIView):
    """
    post:
    Add new question
    """
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    # queryset = Question.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionListView(generics.ListAPIView):
    """
    get:
    Return list of all questions
    """
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class QuestionManageListCreateView(BaseManageView):
    """
    get:
    Return list of all questions

    post:
    Add new question
    """
    VIEWS_BY_METHOD = {
        'GET': QuestionListView.as_view,
        'POST': QuestionCreateView.as_view,
    }

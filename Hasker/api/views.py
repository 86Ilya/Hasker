# from rest_framework import viewsets
from Hasker.profile.models import HaskerUser
from Hasker.hasker.models import Question, Answer
from Hasker.api.serializers import HaskerUserCreateSerializer, QuestionSerializer, HaskerUserUpdateSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.schemas import ManualSchema, AutoSchema
import coreapi


# Create your views here.
class SignUpView(generics.CreateAPIView):
    serializer_class = HaskerUserCreateSerializer


class RetrieveUpdateDestroyProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HaskerUserUpdateSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = HaskerUser.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)


class ProfileManageView(BaseManageView):
    """
    get:
    Return user profile data

    put:
    Update user profile data

    patch:
    Patch user profile data

    post:
    Create a new user instance
    """

    VIEWS_BY_METHOD = {
        'DELETE':  RetrieveUpdateDestroyProfileView.as_view,
        'GET': RetrieveUpdateDestroyProfileView.as_view,
        'PUT': RetrieveUpdateDestroyProfileView.as_view,
        'POST': SignUpView.as_view,
        'PATCH': RetrieveUpdateDestroyProfileView.as_view
    }


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


class QuestionManageView(BaseManageView):
    """
    get:
    Return list of all questions

    post:
    Add new question
    """
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field("extra_field", ...),
        ]
    )
    VIEWS_BY_METHOD = {
        'GET': QuestionListView.as_view,
        'POST': QuestionCreateView.as_view,
    }

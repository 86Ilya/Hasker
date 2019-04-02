from django.urls import path, re_path
from rest_framework.authtoken import views as authviews

from Hasker.api.views.profile_views import ProfileManageView
from Hasker.api.views.hasker_views import QuestionListView, QuestionTrendingListView, QuestionSearchListView
from Hasker.api.views.hasker_views import QuestionByIDView, AnswersListView
from Hasker.api.swagger_schema import SwaggerSchemaView


urlpatterns = [
    path('api/v1/profile/', ProfileManageView.as_view(), name="api_profile"),
    path('api/v1/question/', QuestionListView.as_view(), name='questions_index'),
    path('api/v1/question/trending', QuestionTrendingListView.as_view(), name='questions_trending'),
    re_path('api/v1/question/search/(?P<query>.*?)/$', QuestionSearchListView.as_view(), name='questions_search'),
    re_path('api/v1/question/(?P<id>\d*?)/$', QuestionByIDView.as_view(), name='question_by_id'),
    re_path('api/v1/question/(?P<id>\d*?)/answer/$', AnswersListView.as_view(), name='answers'),
    path('api/v1/auth/', authviews.obtain_auth_token, name='authenticate'),
    path('api/v1/docs/', SwaggerSchemaView.as_view())
]

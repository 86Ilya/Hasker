from rest_framework.authtoken import views as authviews
from Hasker.api import views
from django.urls import path
from Hasker.api.swagger_schema import SwaggerSchemaView


urlpatterns = [
    path('api/v1/profile/', views.ProfileManageView.as_view(), name="api_profile"),
    path('api/v1/question/', views.QuestionManageListCreateView.as_view()),
    # re_path('api/v1/question/(?P<id>\d*)', views.QuestionView.as_view()),
    path('api/v1/auth/', authviews.obtain_auth_token),
    path('docs/', SwaggerSchemaView.as_view())
]

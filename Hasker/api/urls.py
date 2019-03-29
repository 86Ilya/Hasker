from rest_framework.authtoken import views as authviews
from Hasker.api import views
from django.urls import path, re_path
from Hasker.api.swagger_schema import SwaggerSchemaView

# from Hasker.api.swagger import schema_view
# from rest_framework.schemas import get_schema_view
# schema_view = get_schema_view(title="Example API")
# schema_view = get_swagger_view(title='Hasker API')

urlpatterns = [
    path('api/v1/profile/', views.ProfileManageView.as_view()),
    path('api/v1/question/', views.QuestionManageView.as_view()),
    path('api/v1/question/', views.QuestionCreateView.as_view()),
    # re_path('api/v1/question/(?P<id>\d*)', views.QuestionView.as_view()),
    # path('api/v1/profile/', views.SignUpView.as_view()),
    path('api/v1/auth/', authviews.obtain_auth_token),
    path('docs/', SwaggerSchemaView.as_view())
]

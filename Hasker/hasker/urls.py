from Hasker.hasker import views
from django.urls import path, re_path

urlpatterns = [
    path(r'ask/', views.ask_view, name="ask"),
    re_path(r'^question(?P<question_id>(\d*))/(?P<vote>(dislike|like))', views.question_vote, name="question"),
    re_path(r'^question(?P<question_id>(\d*))/', views.question_view, name="question"),
    re_path(r'^search/(?P<query>.*?)/', views.search_view, name="search"),
    re_path(r'^tag/(?P<tag>.*?)/', views.search_by_tag_view, name="search_by_tag"),
    re_path(r'^answer(?P<answer_id>(\d*))/(?P<vote>(dislike|like))', views.answer_vote, name="answer_vote"),
    re_path(r'^answer(?P<answer_id>(\d*))/(?P<star>(add_star|remove_star))', views.answer_star, name="answer_star"),
    re_path(r'^(?P<order>(hot_questions)?)$', views.main_view, name="mainpage"),
    path(r'', views.main_view, name="mainpage"),
    ]

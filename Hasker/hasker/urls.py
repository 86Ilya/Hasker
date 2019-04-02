from django.urls import path, re_path

from Hasker.hasker import views

urlpatterns = [
    path(r'ask/', views.ask_view, name="ask"),
    re_path(r'^question(?P<question_id>(\d*))/(?P<vote>(dislike|like))', views.question_vote, name="question_vote"),
    re_path(r'^question(?P<question_id>(\d*))/', views.question_view, name="question"),
    re_path(r'^search/(?P<query>.*?)/', views.search_view, name="search"),
    re_path(r'^tag/(?P<tag>.*?)/', views.search_by_tag_view, name="search_by_tag"),
    re_path(r'^answer(?P<answer_id>(\d*))/(?P<vote>(dislike|like))', views.answer_vote, name="answer_vote"),
    re_path(r'^answer(?P<answer_id>(\d*))/(?P<star>(add_star|remove_star))', views.answer_star, name="answer_star"),
    path(r'hot_questions/', views.main_view, {'order': 'hot_questions'}, name="mainpage_hot_questions"),
    path(r'', views.main_view, name="mainpage"),
]

handler404 = 'Hasker.profile.views.handler404'
handler500 = 'Hasker.profile.views.handler500'

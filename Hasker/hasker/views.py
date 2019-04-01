from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator

from Hasker.hasker.forms import AskForm, AnswerForm
from Hasker.hasker.models import Tag, Question, Answer
from Hasker.httpcodes import HTTP_BAD_REQUEST, HTTP_NOT_FOUND, HTTP_OK, HTTP_UNAUTHORIZED
from Hasker.helpers import base, send_email_with_link_to_question
from Hasker.settings import QUESTIONS_PER_PAGE, ANSWERS_PER_PAGE, MAX_LENGTH_SEARCH
from Hasker.hasker.helpers import save_answer_from_request, save_question_from_request

User = get_user_model()


def main_view(request, order=None):
    context = base(request)
    if order == 'hot_questions':
        questions_list = Question.objects.all().order_by('likes', '-dislikes')
    else:
        questions_list = Question.objects.all().order_by('-creation_date')
    paginator = Paginator(questions_list, QUESTIONS_PER_PAGE)
    page = request.GET.get('page')
    questions = paginator.get_page(page)

    context.update({'questions': questions})
    return render(request, "mainpage.html", context)


def search_view(request, query):
    context = base(request)
    # TODO SQL INJECTION???

    context.update({'search_header': 'Search result'})

    if len(query) > MAX_LENGTH_SEARCH:
        context.update({'questions': []})
        return render(request, "search.html", context, status=HTTP_BAD_REQUEST)

    questions_list = Question.objects.filter(Q(content__contains=query) | Q(header__contains=query))

    if len(questions_list) == 0:
        context.update({'questions': []})
        return render(request, "search.html", context, status=HTTP_NOT_FOUND)

    paginator = Paginator(questions_list, QUESTIONS_PER_PAGE)
    page = request.GET.get('page')
    questions = paginator.get_page(page)

    context.update({'questions': questions})
    return render(request, "search.html", context)


def search_by_tag_view(request, tag):
    context = base(request)
    context.update({'search_header': 'Search by tag result'})
    tag_obj = Tag.objects.filter(tag_name=tag).first()

    if tag_obj:
        questions_list = Question.objects.filter(tags=tag_obj).order_by('likes', '-dislikes')

        paginator = Paginator(questions_list, QUESTIONS_PER_PAGE)
        page = request.GET.get('page')
        questions = paginator.get_page(page)

        context.update({'questions': questions})
        return render(request, "search.html", context)
    else:
        context.update({'questions': []})
        return render(request, "search.html", context, status=HTTP_NOT_FOUND)


@login_required
def ask_view(request):
    context = base(request)
    context.update({'exist_tags': Tag.objects.all()})
    status = HTTP_OK

    if request.method == "POST":
        question = save_question_from_request(request, context)
        if question:
            return redirect(reverse('question', kwargs={'question_id': question.id}))
        else:
            status = HTTP_BAD_REQUEST
    else:
        context.update({'form': AskForm})
    return render(request, 'ask.html', context, status=status)


def question_view(request, question_id):
    context = base(request)
    question = get_object_or_404(Question, id=question_id)
    status = HTTP_OK
    # adding answer
    if request.method == "POST":
        if context["user"] is None:
            return render(request, 'question.html', context, status=HTTP_UNAUTHORIZED)
        answer = save_answer_from_request(request, context, question)
        if answer:
            link = send_email_with_link_to_question(question, answer)
            return redirect(link)
        else:
            status = HTTP_BAD_REQUEST
    elif request.method == "GET":
        # blank form
        context.update({'form': AnswerForm})

    answers_list = Answer.objects.filter(question=question)
    paginator = Paginator(answers_list, ANSWERS_PER_PAGE)
    page = request.GET.get('page')
    answers = paginator.get_page(page)

    context.update({'question': question, 'answers': answers})
    return render(request, 'question.html', context, status=status)


@login_required
def question_vote(request, question_id, vote):
    question = Question.objects.get(id=question_id)
    user = User.objects.get(pk=request.user.pk)
    result = question.vote(user, vote)
    rating = question.get_rating()
    context = {'result': result, 'rating': rating}
    return JsonResponse(context)


@login_required
def answer_vote(request, answer_id, vote):
    answer = Answer.objects.get(id=answer_id)
    user = User.objects.get(pk=request.user.pk)
    result = answer.vote(user, vote)
    rating = answer.get_rating()
    context = {'result': result, 'rating': rating}
    return JsonResponse(context)


@login_required
def answer_star(request, answer_id, star):
    answer = Answer.objects.get(id=answer_id)
    user = User.objects.get(pk=request.user.pk)
    result = answer.move_star(user, star)
    correct = answer.correct()

    context = {'result': result, 'correct': correct}
    return JsonResponse(context)

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail

from Hasker.hasker.forms import AskForm, AnswerForm
from Hasker.hasker.models import Tag, Question, Answer
from Hasker.settings import EMAIL_HOST_USER
from Hasker.httpcodes import *

TRENDING_QUESTIONS = 20
QUESTIONS_PER_PAGE = 20
ANSWERS_PER_PAGE = 30
MAX_LENGTH_SEARCH = 1024
User = get_user_model()


def base(request):
    """
    :param request:
    :return dict: Возвращает базовый контекст для всех страниц
    """
    # username = None
    # avatar = None
    context = dict()
    trending_questions = Question.objects.all().order_by('likes', '-dislikes')[:TRENDING_QUESTIONS]
    context.update({'trending_questions': trending_questions})
    if not request.user.is_anonymous:
        user = User.objects.get(pk=request.user.pk)
        context.update({"user": user})
    else:
        context.update({"user": None})
    return context


# Create your views here.
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
    user = context['user']
    context.update({'exist_tags': Tag.objects.all()})
    status = HTTP_OK

    if request.method == "POST":

        ask_form = AskForm(request.POST)
        context.update({'form': ask_form})
        if ask_form.is_valid():

            ask_form.author = user
            question = ask_form.save(commit=False)

            question.author = user
            question.save()
            ask_form.save_m2m()

            return redirect(reverse('question', kwargs={'question_id': question.id}))
        else:
            status = HTTP_BAD_REQUEST
    else:
        context.update({'form': AskForm})
    return render(request, 'ask.html', context, status=status)


def question_view(request, question_id):
    context = base(request)
    question = get_object_or_404(Question, id=question_id)
    user = context["user"]

    status = HTTP_OK
    # adding answer
    if request.method == "POST":
        # TODO am I need to login?
        if user is None:
            return render(request, 'question.html', context, status=HTTP_UNAUTHORIZED)
        answer_form = AnswerForm(request.POST)
        context.update({'form': answer_form})

        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.author = user
            answer.question = question
            answer.save()
            # send email to question author
            email_recepient = question.author.email

            num_pages = question.get_answers_count() // QUESTIONS_PER_PAGE
            last_page = 1 if num_pages == 0 else num_pages
            link = '/question{}/?page={}#answer{}'.format(question.id, last_page, answer.id)
            subject = "You have new answer for your question {}".format(question.header)
            content = "Link for answer: http://localhost:8000/" + link
            # Отправитель и получатель - одно лицо, сделано для отладки. TODO
            send_mail(subject, content, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False)

            # return redirect(reverse('question', kwargs={'question_id': question.id}))
            # TODO is redirect is normal?
            return redirect(link)
        else:
            status = HTTP_BAD_REQUEST

    else:
        # blank form
        context.update({'form': AnswerForm})

    answers_list = Answer.objects.filter(question=question)

    paginator = Paginator(answers_list, ANSWERS_PER_PAGE)
    page = request.GET.get('page')
    answers = paginator.get_page(page)

    context.update({'question': question})
    context.update({'answers': answers})
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

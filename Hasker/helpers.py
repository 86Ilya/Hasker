from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from Hasker.settings import EMAIL_HOST_USER
from Hasker.hasker.models import Question

User = get_user_model()

TRENDING_QUESTIONS = 20
QUESTIONS_PER_PAGE = 20
ANSWERS_PER_PAGE = 30
MAX_LENGTH_SEARCH = 1024


def base(request):
    """
    :param request:
    :return dict: Возвращает базовый контекст для всех страниц
    """
    context = dict()
    trending_questions = Question.objects.all().order_by('likes', '-dislikes')[:TRENDING_QUESTIONS]
    context.update({'trending_questions': trending_questions})
    if not request.user.is_anonymous:
        user = User.objects.get(pk=request.user.pk)
        context.update({"user": user})
    else:
        context.update({"user": None})
    return context


def send_email_with_link_to_question(question, answer):
    num_pages = question.get_answers_count() // QUESTIONS_PER_PAGE
    last_page = 1 if num_pages == 0 else num_pages
    link = '/question{}/?page={}#answer{}'.format(question.id, last_page, answer.id)
    subject = "You have new answer for your question {}".format(question.header)
    content = "Link for answer: http://localhost:8000/" + link
    # Отправитель и получатель - одно лицо, сделано для отладки. TODO
    send_mail(subject, content, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False)
    return link

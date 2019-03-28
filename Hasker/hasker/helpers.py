from Hasker.hasker.forms import AskForm, AnswerForm


def save_question_from_request(request, context):
    user = context['user']
    ask_form = AskForm(request.POST)
    context.update({'form': ask_form})
    if ask_form.is_valid():
        ask_form.author = user
        question = ask_form.save(commit=False)
        question.author = user
        question.save()
        ask_form.save_m2m()
        return question


def save_answer_from_request(request, context, question):
    user = context['user']
    if user is None:
        return
    answer_form = AnswerForm(request.POST)
    context.update({'form': answer_form})

    if answer_form.is_valid():
        answer = answer_form.save(commit=False)
        answer.author = user
        answer.question = question
        answer.save()
        return answer

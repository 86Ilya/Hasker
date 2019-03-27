from django.db import models
from django.utils import timezone

from Hasker.profile.models import HaskerUser


class LikesMixin:
    def get_rating(self):
        likes = self.likes.all().count()
        dislikes = self.dislikes.all().count()
        return likes - dislikes

    def like(self, user):
        exist_dislike = self.dislikes.filter(username=user.username).first()
        exist_like = self.likes.filter(username=user.username).first()
        if exist_dislike:
            self.dislikes.remove(user)
        elif not exist_like:
            self.likes.add(user)
        else:
            return
        return True

    def dislike(self, user):
        exist_dislike = self.dislikes.filter(username=user.username).first()
        exist_like = self.likes.filter(username=user.username).first()
        if exist_like:
            self.likes.remove(user)
        elif not exist_dislike:
            self.dislikes.add(user)
        else:
            return
        return True

    def vote(self, user, vote):
        result = None
        if vote.lower() == 'like':
            result = self.like(user)
        elif vote.lower() == 'dislike':
            result = self.dislike(user)

        return result


class Tag(models.Model):
    tag_name = models.CharField(max_length=64)


class Question(LikesMixin, models.Model):
    header = models.CharField(max_length=256)
    content = models.CharField(max_length=1024)
    author = models.ForeignKey(HaskerUser, related_name='question_author', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name='tags', default=None)
    likes = models.ManyToManyField(HaskerUser, default=None, related_name="question_likes")
    dislikes = models.ManyToManyField(HaskerUser, default=None, related_name="question_dislikes")
    correct_answer = models.ForeignKey('Answer', default=None, blank=True, null=True, related_name='correct_answer', on_delete=models.CASCADE)

    def get_answers(self):
        answers = Answer.objects.filter(question=self)
        return answers

    def get_answers_count(self):
        return self.get_answers().count()

    def get_tags(self):
        return list(self.tags.values())

    def __str__(self):
        return "Question '{}'".format(self.header)


class Answer(LikesMixin, models.Model):
    content = models.CharField(max_length=1024)
    author = models.ForeignKey(HaskerUser, related_name='answer_author', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.ManyToManyField(HaskerUser, default=None, related_name="answer_likes")
    dislikes = models.ManyToManyField(HaskerUser, default=None, related_name="answer_dislikes")

    class Meta:
        ordering = ['creation_date']

    def correct(self):
        question = Question.objects.get(answer=self)
        return question.correct_answer == self

    def move_star(self, user, star):
        result = None
        question = Question.objects.get(answer=self)
        iamcorrect = question.correct_answer == self

        if user != question.author:
            return result

        if star.lower() == 'add_star' and iamcorrect is False:
            question.correct_answer = self
            question.save()
            result = True
        elif star.lower() == 'remove_star' and iamcorrect:
            question.correct_answer = None
            question.save()
            result = True

        return result

    def __str__(self):
        return "Answer '{:.128}'...".format(self.content)

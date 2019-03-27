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
            # TODO
            return False
        return True

    def dislike(self, user):
        exist_dislike = self.dislikes.filter(username=user.username).first()
        exist_like = self.likes.filter(username=user.username).first()
        if exist_like:
            self.likes.remove(user)
        elif not exist_dislike:
            self.dislikes.add(user)
        else:
            # TODO
            return False
        return True


class ReprDateMixin:
    def get_relation_creation_time_str(self):
        now = timezone.now()
        delta = now - self.creation_date
        if delta.days >= 1:
            return "{} days ago".format(delta.days)
        else:
            if delta.seconds < 60:
                return "{} seconds ago".format(delta.seconds)
            if 60 < delta.seconds < 60 * 60:
                return "{} minutes ago".format(delta.seconds // 60)

            return "{} hours ago".format(delta.seconds // (60 * 60))


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

    def get_answers(self):
        answers = Answer.objects.filter(question=self)
        return answers

    def get_answers_count(self):
        return self.get_answers().count()

    def get_tags(self):
        return list(self.tags.values())


class Answer(LikesMixin, models.Model):
    content = models.CharField(max_length=1024)
    author = models.ForeignKey(HaskerUser, related_name='answer_author', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.ManyToManyField(HaskerUser, default=None, related_name="answer_likes")
    dislikes = models.ManyToManyField(HaskerUser, default=None, related_name="answer_dislikes")

    class Meta:
        ordering = ['creation_date']

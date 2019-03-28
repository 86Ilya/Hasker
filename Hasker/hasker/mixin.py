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

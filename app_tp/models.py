from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum


class LikeManager(models.Manager):
    pass


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)

    value = models.SmallIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = LikeManager()


class TagManager(models.Manager):
    pass


class QuestionManager(models.Manager):
    def get_questions_ordered_by_date(self):
        return self.all().order_by('-date')


    def get_questions_ordered_by_rating(self):
        return self.all().order_by('-rating')


    def get_questions_by_tag(self, tag_id):
        return self.filter(tags__id=tag_id)


class AnswerManager(models.Manager):
    def get_answers_by_question(self, question_id):
        return self.filter(question__id=question_id)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    objects = TagManager()

    def __str__(self): return f"{self.name} "


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)
    objects = QuestionManager()

    rating = models.IntegerField(default=0)
    def __str__(self): return f"{self.title} {self.user.username} {self.date} {self.rating}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # user_login = models.CharField(max_length=100) - вместо него и так есть username
    nickname = models.CharField(max_length=100)
    # будет разбираться в 5 дз
    # avatar = models.ImageField(blank=True)
    user_rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} {self.nickname}"



class Answer(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    correct = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    likes = GenericRelation(Like)
    objects = AnswerManager()

    rating = models.IntegerField(default=0)

    def __str__(self): return f"{self.user.username} {self.question}"

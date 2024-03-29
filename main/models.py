import random, string

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from ckeditor.fields import RichTextField


class Quiz(models.Model):
    title = RichTextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, blank=True, unique=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    @property
    def all_questions(self):
        return self.questions.count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.code = "".join(random.sample(string.ascii_letters, 20))
        super(Quiz, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    title = models.TextField()

    @property
    def correct_answer(self, *args, **kwargs):
        try:
            data = Option.objects.get(question_id=self.id, is_correct=True)   
        except:
            data = False
        return data

    @property
    def get_options(self, *args, **kwargs):
        options = list(Option.objects.filter(question_id=self.id))
        random.shuffle(options)
        return options

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    name = models.TextField()
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            option = Option.objects.filter(question=self.question, is_correct=True)
            if option and self.is_correct:
                raise ValueError('Ikkita to`g`ri javob kiritish mumkin emas')
            elif not option and not self.is_correct :
                raise ValueError('Birinchi to`g`ri javob kiriting ')
        super(Option, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.question.title} -- {self.name}"


class QuizTaker(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Answer(models.Model):
    taker = models.ForeignKey(QuizTaker, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def save(self, *args, **kwargs):
        self.is_correct = self.answer == self.question.correct_answer
        super(Answer, self).save(*args, **kwargs)


class Result(models.Model):
    taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    incorrect_answers = models.IntegerField()

    @property
    def questions(self, *args, **kwargs):
        quiz = self.taker.quiz
        result = Question.objects.filter(quiz=quiz).count()
        return result
    
    @property
    def percentage(self, *args, **kwargs):
        return self.correct_answers / self.questions * 100
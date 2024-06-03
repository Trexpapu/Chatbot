from django.db import models

# Create your models here.
class Answer(models.Model):
    answerID = models.BigAutoField(primary_key=True)
    answer = models.TextField(blank=False, null = False)

class Question(models.Model):
    questionID = models.BigAutoField(primary_key=True)
    question = models.TextField(blank=False, null = False)
    answerID = models.ForeignKey(Answer, on_delete = models.CASCADE)
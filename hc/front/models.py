from django.db import models

# Create your models here.

class FaqQuestions(models.Model):
    """ 
    The models that will hold the faq questions and answers
    """
    questions = models.CharField(max_length=250)
    answer = models.CharField(max_length=250)
    link = models.CharField(max_length=300, blank=True)


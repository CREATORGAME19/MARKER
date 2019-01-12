from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import *
class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    school = models.CharField(max_length=200)
    output = models.TextField()
    input = models.TextField()
    keyterms = models.TextField()
    students = models.TextField()
    marks = models.TextField()

    def get_school(self):
        return self.school
    
    def publish(self):
        self.save()

    def __str__(self):
        return self.title




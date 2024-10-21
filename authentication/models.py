from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class LastLogin(models.Model):
    worker=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(default=datetime.now())
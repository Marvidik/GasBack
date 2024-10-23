from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Amount(models.Model):
    price=models.IntegerField()



class Product(models.Model):
    quantity=models.IntegerField()




class Sales(models.Model):
    worker=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.CharField(max_length=20)
    phone=models.CharField(max_length=15)
    amount_bought=models.IntegerField()
    amount_paid=models.IntegerField()
    payment_option=models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)



class Expenses(models.Model):
    amount=models.IntegerField()
    use=models.CharField(max_length=20)

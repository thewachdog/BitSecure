from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length = 250)
    email=models.CharField(max_length = 250)
    firstname=models.CharField(max_length = 250)
    lastname=models.CharField(max_length = 250)
    password=models.CharField(max_length = 250)
    plan=models.CharField(max_length = 250)

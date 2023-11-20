from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length = 250)
    email=models.CharField(max_length = 250)
    firstname=models.CharField(max_length = 250)
    lastname=models.CharField(max_length = 250)
    password=models.CharField(max_length = 250)
    plan=models.CharField(max_length = 250)

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    url = models.CharField(default = '', max_length=100)

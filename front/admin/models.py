from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField('username', max_length=256, primary_key=True)
    password = models.CharField('hashed password', max_length=256)

from django.db import models
from datetime import datetime

# Create your models here.

class message(models.Model):
    time=models.DateTimeField(default=datetime(2018,9,13,0,0,0))
    info=models.TextField(default='')

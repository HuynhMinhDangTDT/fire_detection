from django.db import models

# Create your models here.

class information(models.Model):
    UserName = models.CharField(max_length = 50,null = True,default = '')

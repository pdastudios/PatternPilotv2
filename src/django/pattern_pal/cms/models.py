from django.db import models

# Create your models here.
class Shape(models.Model):
    project = models.CharField(max_length=255)
    shape_name = models.CharField(max_length=255)
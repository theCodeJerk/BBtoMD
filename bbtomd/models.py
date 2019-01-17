from django.db import models

# Create your models here.
class ConversionModel(models.Model):
    bbcodes = models.TextField()

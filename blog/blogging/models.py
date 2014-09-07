from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel

class Blog(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
	    return self.title

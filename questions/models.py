from django.db import models

# Create your models here.

class Question(models.Model):
    text = models.TextField()
    isAccepted = models.BooleanField(null=True, blank=True, default=None)
    channelName = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)
        return self

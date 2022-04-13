from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Chore(models.Model):
    chore_name = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_due = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.chore_name

    def get_absolute_url(self):
        return reverse('chore-detail', kwargs={'pk' : self.pk})

    


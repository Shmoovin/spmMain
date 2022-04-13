from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

'''This defines the team table.'''
class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)
    team_pswd = models.CharField(max_length=15)

    def __str__(self):
        return self.team_name


class Team_Chore(models.Model):
    team_chore_name = models.CharField(max_length=100, verbose_name='Group Task Name')
    content = models.TextField(verbose_name='Task Content')
    date_created = models.DateField(auto_now_add=True)
    date_due = models.DateField(verbose_name='Due Date')
    is_complete = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.team_chore_name

    def get_absolute_url(self):
        return reverse('team-task-detail', kwargs={'pk' : self.pk})



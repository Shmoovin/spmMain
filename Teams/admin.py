from django.contrib import admin
from .models import Team, Team_Chore

#this registers the Team model with the admin site
admin.site.register(Team)
admin.site.register(Team_Chore)
'''imports'''
from pyexpat import model
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Team, Team_Chore
from .forms import JoinGroup
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
import csv
from Users.models import Profile

'''defines the my group webpage'''
# @login_required
# def groupTest(request):
#     #team of the current user
#     current_user = request.user.profile.team

#     #a dictionary containing all of the other team members
#     context = {'members' : User.objects.filter(profile__team = current_user).values_list('username', flat=True)}

#     #returns a rendering of the html doc for the page, passes the group memebrs as arguments
#     return render(request, 'Teams/GroupTest.html', context)


class GroupListView(LoginRequiredMixin, ListView):
    model = Team_Chore
    template_name ='Teams/GroupTest.html'
    context_object_name = 'GroupTasks'

    def get_queryset(self, *args, **kwargs):
        qs = Team_Chore.objects.filter(team = self.request.user.profile.team, is_complete = False).order_by('is_complete', 'date_due')
        return qs

class GroupListViewAll(LoginRequiredMixin, ListView):
    model = Team_Chore
    template_name ='Teams/GroupTestAll.html'
    context_object_name = 'GroupTasks'

    def get_queryset(self, *args, **kwargs):
        qs = Team_Chore.objects.filter(team = self.request.user.profile.team).order_by('is_complete', 'date_due')
        return qs


'''defines the join group page'''
@login_required
def join_group(request):

    #if the a post request is made ...
    if request.method == 'POST':
        #creates an instance of the JoinGroup form
        form = JoinGroup(request.POST)

        #if the form has vaild values
        if form.is_valid():

            #if the user is not already in a group
            if request.user.profile.team == None:

                #if the inputed team name and password match an existing group
                if Team.objects.filter(team_name=form.cleaned_data['name']).filter(team_pswd = form.cleaned_data['pswd']).exists():
                    #add the cooresponding group as a foreign key to the user
                    request.user.profile.team = Team.objects.filter(team_name=form.cleaned_data['name']).filter(team_pswd = form.cleaned_data['pswd']).first()
                    #save the update to the user's profile
                    request.user.profile.save()
                    #redirect to the group page
                    return HttpResponseRedirect('/group/')
                else:
                    #if the team name and password do not match an existing group
                    messages.warning(request, 'No Such Group')
            #if the user is already in a group
            else:
                messages.warning(request, 'You are already in a Group')
    
    #if any other type of request is made .. do nothing basically
    else:
      form = JoinGroup()

    #render the html doc for the page, passing the form object as an argument
    return render(request, 'Teams/JoinGroup.html', {'form': form})        



'''class based definition of the create group webpage'''
'''to do add user passes test for not in group'''
class GroupCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    #createView is a django included view to create a form to fill in a table
    #this view creates a new row in the Team (group) table

    #html doc for this view
    template_name = 'Teams/CreateTeam.html'
    #the model (db table) that this createview care about
    model = Team
    #the fields that the created form should use
    fields = ['team_name', 'team_pswd']
    #on successful creation, the user is redirected to the join group page
    success_url = reverse_lazy('group-join')

    def test_func(self):
        has_group = self.request.user.profile.team
        if has_group:
            return False
        else:
            return True



class GroupTaskCreateView(LoginRequiredMixin, CreateView):

    template_name = 'Teams/CreateGroupTask.html'
    model = Team_Chore
    fields = ['team_chore_name', 'content', 'date_due']

    def form_valid(self, form):

        form.instance.creator = self.request.user
        form.instance.team = self.request.user.profile.team
        return super().form_valid(form)

    success_url = reverse_lazy('group-test')

class GroupTaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'Teams/DetailGroupTask.html'
    model = Team_Chore

    def post(self, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="event.csv"'},
        )
        name = list(Team_Chore.objects.filter(**kwargs).values_list('team_chore_name', flat=True))
        date = list(Team_Chore.objects.filter(**kwargs).values_list('date_due', flat=True))
        description = list(Team_Chore.objects.filter(**kwargs).values_list('content', flat=True))

        writer = csv.writer(response)
        writer.writerow(['Subject', 'Start Date', 'End Date', 'Description'])
        writer.writerow([str(name[0]), str(date[0]), str(date[0]), str(description[0])])

        return response

    def test_func(self):
        task = self.get_object()
        if self.request.user.profile.team == task.team:
            return True
        return False

class GroupTaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'Teams/UpdateGroupTask.html'
    model = Team_Chore
    fields = ['team_chore_name', 'content', 'date_due', 'is_complete']
    success_url = reverse_lazy('group-test')

    def test_func(self):
        task = self.get_object()
        if self.request.user.profile.team == task.team:
            return True
        return False

class GroupTaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'Teams/DeleteGroupTask.html'
    model = Team_Chore
    success_url = reverse_lazy('group-test')

    def test_func(self):
        task = self.get_object()
        if self.request.user.profile.team == task.team:
            return True
        return False
    


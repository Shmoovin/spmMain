from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from .models import Chore
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest
from django.utils import timezone
import csv


@login_required
def chore_list(request):
    context = {
        'tasks' : Chore.objects.filter(user=request.user).order_by('is_complete', 'date_due')
    }
    return render(request, 'chores/chore_list.html', context)



class ChoreListView(LoginRequiredMixin, ListView):
    model = Chore
    template_name = 'chores/chore_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self, *args, **kwargs):
        qs = Chore.objects.all().order_by('is_complete', 'date_due')
        qs = qs.filter(user = self.request.user)
        return qs

class IncompleteChoreListView(LoginRequiredMixin, ListView):
    model = Chore
    template_name = 'chores/chore_list_incomplete.html'
    context_object_name = 'tasks'
    
    def get_queryset(self, *args, **kwargs):
        qs = Chore.objects.filter(is_complete = False).order_by('is_complete', 'date_due')
        qs = qs.filter(user = self.request.user)
        return qs


class ChoreDetailView(LoginRequiredMixin, DetailView):
    model = Chore

    def post(self, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="event.csv"'},
        )
        name = list(Chore.objects.filter(**kwargs).values_list('chore_name', flat=True))
        date = list(Chore.objects.filter(**kwargs).values_list('date_due', flat=True))
        description = list(Chore.objects.filter(**kwargs).values_list('content', flat=True))

        writer = csv.writer(response)
        writer.writerow(['Subject', 'Start Date', 'End Date', 'Description'])
        writer.writerow([str(name[0]), str(date[0]).strip(' 00:00:00+00:00'), str(date[0]).strip(' 00:00:00+00:00'), str(description[0])])

        return response

class ChoreCreateView(LoginRequiredMixin, CreateView):
    model = Chore
    fields = ['chore_name', 'content', 'date_due']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChoreUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Chore
    fields = ['chore_name', 'content', 'date_due', 'is_complete']

    def test_func(self):
        chore = self.get_object()
        if self.request.user == chore.user:
            return True
        return False
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ChoreDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Chore
    success_url = reverse_lazy('chore-home')

    def test_func(self):
        chore = self.get_object()
        if self.request.user == chore.user:
            return True
        return False





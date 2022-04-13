from django.urls import path
from .views import ChoreListView, ChoreDetailView, ChoreCreateView, ChoreUpdateView, ChoreDeleteView, IncompleteChoreListView
from . import views

urlpatterns = [
    path('', IncompleteChoreListView.as_view(), name='chore-home'),
    path('all/', ChoreListView.as_view(), name='chore-all'),
    path('<int:pk>/', ChoreDetailView.as_view(), name='chore-detail'),
    path('new/', ChoreCreateView.as_view(), name='chore-create'),
    path('<int:pk>/update/', ChoreUpdateView.as_view(), name='chore-update'),
    path('<int:pk>/delete/', ChoreDeleteView.as_view(), name='chore-delete'),

]
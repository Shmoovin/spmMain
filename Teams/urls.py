from django.urls import path
from . import views
from .views import GroupCreateView, GroupTaskCreateView, GroupListView, GroupTaskDetailView, GroupTaskUpdateView, GroupTaskDeleteView, GroupListViewAll

#this list defines the extentions to any url starting with /group/...
urlpatterns = [
    #path('', views.groupTest, name='group-test'), #/group/
    path('', GroupListView.as_view(), name='group-test'),
    path('all/', GroupListViewAll.as_view(), name='group-test-all'),
    path('join/', views.join_group, name='group-join'), #/group/join/
    path('create/', GroupCreateView.as_view(), name='group-create' ), #/group/create
    path('create_task/', GroupTaskCreateView.as_view(), name='team-task-create'),
    path('task/<int:pk>/',GroupTaskDetailView.as_view(), name='team-task-detail'),
    path('task/<int:pk>/update/',GroupTaskUpdateView.as_view(), name='team-task-update'),
    path('task/<int:pk>/delete/',GroupTaskDeleteView.as_view(), name='team-task-delete'),

]
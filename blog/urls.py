from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    #PostUpdateView,
    PostDeleteView,
    UserPostListView,
    Work
    ,
    create
    ,
    UserPostList
)
from . import views
#
urlpatterns = [
    path('', UserPostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/<str:username>', UserPostList.as_view(), name='user-posts'),
    path('user/', Work.as_view(), name='work'),
    path('post/new/', create, name='post-create'),
    path('post/<int:pk>/update/', views.update, name='post-update'),
    #path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('all/', views.admi, name='team'),
    path('all/<str:name>',views.teammembers,name='teammembers'),
    
]

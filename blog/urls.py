from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    #PostCreateView,
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
    path('hom',create,name="hom"),
    path('home', UserPostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/<str:username>', UserPostList.as_view(), name='user-posts'),
    path('user/', Work.as_view(), name='work'),
    path('post/new/', create, name='post-create'),
    path('post/<int:pk>/update/', views.update, name='post-update'),
    path('', views.admi, name='team'),
    path('<str:name>',views.teammembers,name='teammembers'),
    path('user/password/<str:name>',views.changepass,name='password')    
]

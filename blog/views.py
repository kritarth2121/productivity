from django.shortcuts import render, get_object_or_404,redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta

import datetime
from django.utils import timezone
from users import views as user_views
from users.models import Profile
from .models import Post,Team
from django.db.models.functions import datetime
import datetime

from django.contrib.admin import widgets                                       
from django.contrib.auth.decorators import user_passes_test
def home(request):
    if request.user.is_superuser:
        
        context = {
            'posts': Post.objects.all()
        }
        print(context)
        return render(request, 'blog/home.html', context)
    if request.user.is_authenticated:
        user=request.user.id
        context = {
            'posts': Post.objects.filter(assigned_employee=user)
        }
        return render(request, 'blog/home.html', context)
    else:

        return render(request, 'login')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
@login_required
def admi(request):
    if request.user.is_superuser==True:
        context = {
                'team':Team.objects.filter(owner=request.user),

            }
        print(context)
        
        return render(request, 'blog/team.html', context)
    else:
        return redirect('hom')

def teammembers(request,name):
    if request.user.is_superuser:
        context = {
                'team': Profile.objects.filter(team__name=name),

            }
        
        print(context)
        return render(request, 'blog/teammembers.html', context)
    else:
        return redirect('hom')



class UserPost(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    currentTime = datetime.datetime.now() 

    def get_queryset(self):
        print(self.request.user)
        print(Post.objects.all())
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        user = get_object_or_404(User, username=self.request.user)
        return Post.objects.filter(assigned_employee__username=user).order_by('-date_posted')
    

class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    currentTime = datetime.datetime.now() 

    def get_queryset(self):
        print(self.request.user)
        print(Post.objects.all())
        #user = get_object_or_404(User, username=self.kwargs.get('username'))
        user = get_object_or_404(User, username=self.request.user)
        return Post.objects.filter(assigned_employee__username=user).order_by('-date_posted')
class UserPostList(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    currentTime = datetime.datetime.now() 

    def get_queryset(self):
        print(self.request.user)
        print(Post.objects.all())
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        #user = get_object_or_404(User, username=self.request.user)
        return Post.objects.filter(assigned_employee__username=user).order_by('-date_posted')

class Work(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        
        return Post.objects.filter(assigned_employee__username=self.request.user).order_by('-date_posted')
        
class PostDetailView(ListView):
    model = Post
    
    template_name = 'blog/post_detail.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    currentTime = datetime.datetime.now() 
    def get_queryset(self):
        user = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        print(user.id)
        return Post.objects.filter(id=user.id)



@login_required
def create(request):
    for i in range(10):
        print(i)
    print(Post.objects.filter(date_posted__day=(datetime.datetime.now().day -1),date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user))
    if Post.objects.filter(date_posted__day=datetime.datetime.now().day , date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==0  or Post.objects.filter(date_posted__day=datetime.datetime.now().day , date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==1   :

        if int(datetime.datetime.now().hour)>=6 and int(datetime.datetime.now().hour)<=13:
            if request.method == 'POST':
                today=request.POST['today']
                if Post.objects.filter(date_posted__day=datetime.datetime.now().day,date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==0:
                    ins=Post.objects.create(work_today=today,assigned_employee=request.user,date_posted=datetime.datetime.now())
                    ins.save()
                    return redirect('hom')
                elif Post.objects.filter(date_posted__day=datetime.datetime.now().day,date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==1:
                    insta=Post.objects.get(date_posted__day=datetime.datetime.now().day,date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user)
                    insta.work_today=today
                    insta.save()
                    return redirect('hom')

                else:
                    postss= Post.objects.filter(assigned_employee=request.user).order_by('-date_posted')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(postss, 7)
                    try:
                        posts = paginator.page(page)
                    except PageNotAnInteger:
                        posts = paginator.page(1)
                    except EmptyPage:
                        posts = paginator.page(paginator.num_pages)
                    
                    return render(request, 'blog/user_post.html', {'posts': posts})
            else:
                    postss= Post.objects.filter(assigned_employee=request.user).order_by('-date_posted')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(postss, 7)
                    try:
                        posts = paginator.page(page)
                    except PageNotAnInteger:
                        posts = paginator.page(1)
                    except EmptyPage:
                        posts = paginator.page(paginator.num_pages)
                    
                    return render(request, 'blog/user_post.html', {'posts': posts})
        elif (int(datetime.datetime.now().hour)>=18 and int(datetime.datetime.now().hour)<=24) or (int(datetime.datetime.now().hour)>=0 and int(datetime.datetime.now().hour<=3)):
            if request.method == 'POST':
                today=request.POST['today']
                if Post.objects.filter(date_posted__day=datetime.datetime.now().day,date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==1 and (int(datetime.datetime.now().hour)>=18):
                    insta=Post.objects.get(date_posted__day=datetime.datetime.now().day,date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user)
                    insta.work_done=today
                    insta.save()
                    print("created")
                    
                    return redirect('hom')
                elif Post.objects.filter(date_posted__day=(datetime.datetime.now().day -1),date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==1 and (int(datetime.datetime.now().hour)>=0 and int(datetime.datetime.now().hour<=3)):
                    insta=Post.objects.get(date_posted__day=(datetime.datetime.now().day -1),date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user)
                    insta.work_done=today
                    print("created00000")

                    insta.save()
                    return redirect('hom')
                elif Post.objects.filter(date_posted__day=(datetime.datetime.now().day-1),date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==0 and (int(datetime.datetime.now().hour)>=0 and int(datetime.datetime.now().hour<=3)):
                    ins=Post.objects.create(work_done=today,assigned_employee=request.user,date_posted=(timezone.now() - timedelta(1)))
                    ins.save()
                    return redirect('hom')
                elif Post.objects.filter(date_posted__day=datetime.datetime.now().day,date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year,assigned_employee=request.user).count()==0 :
                    ins=Post.objects.create(work_done=today,assigned_employee=request.user,date_posted=datetime.datetime.now())
                    ins.save()
                    return redirect('hom')
                else:
                    postss= Post.objects.filter(assigned_employee=request.user).order_by('-date_posted')
                    page = request.GET.get('page', 1)

                    paginator = Paginator(postss, 7)
                    try:
                        posts = paginator.page(page)
                    except PageNotAnInteger:
                        posts = paginator.page(1)
                    except EmptyPage:
                        posts = paginator.page(paginator.num_pages)
                    
                    return render(request, 'blog/user_post.html', {'posts': posts})

            else:
                postss= Post.objects.filter(assigned_employee=request.user).order_by('-date_posted')
                page = request.GET.get('page', 1)

                paginator = Paginator(postss, 7)
                try:
                    posts = paginator.page(page)
                except PageNotAnInteger:
                    posts = paginator.page(1)
                except EmptyPage:
                    posts = paginator.page(paginator.num_pages)
                    
                return render(request, 'blog/user_post.html', {'posts': posts})
                
        else:
            postss= Post.objects.filter(assigned_employee=request.user).order_by('-date_posted')
            page = request.GET.get('page', 1)

            paginator = Paginator(postss, 7)
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
                    
            return render(request, 'blog/user_post.html', {'posts': posts})

                    
    else:
        postss= Post.objects.filter(assigned_employee=request.user).order_by('-date_posted')
        page = request.GET.get('page', 1)

        paginator = Paginator(postss, 7)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
                    
        return render(request, 'blog/user_post.html', {'posts': posts})
@login_required
def update(request,pk):
        print(datetime.datetime.now().hour)
        if Post.objects.get(id=pk).date_posted.day==datetime.datetime.now().day or (Post.objects.get(id=pk).date_posted.day==(datetime.datetime.now().day-1) and datetime.datetime.now().hour<=3):
            if int(datetime.datetime.now().hour)>=6 and int(datetime.datetime.now().hour)<=13:
                if request.method == 'POST':
                    today=request.POST['today']
                    ins=Post.objects.get(id=pk)
                    ins.work_today=today
                    ins.save()
                    return redirect('hom')
                else:
                    return render(request, "blog/post_form.html" )
            elif (int(datetime.datetime.now().hour)>=18 and int(datetime.datetime.now().hour)<=24) or (int(datetime.datetime.now().hour)>=0 and int(datetime.datetime.now().hour<=3)):
                if request.method == 'POST':
                    today=request.POST['today']
                    if Post.objects.filter(id=pk).count()==1:
                        insta=Post.objects.get(id=pk)
                        insta.work_done=today
                        insta.save()
                        print("created")
                        
                        return redirect('hom')
                else:
                    insta=Post.objects.get(id=pk)
                    context={
                        'post':insta.work_today
                    }
                    return render(request, "blog/post_form1.html" ,context)
            else:
                return render(request,"blog/return.html")
        else:
            return render(request,"blog/cantupdate.html")

            

    

        


    #print(post.id)

     
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        
        if self.request.user.is_superuser:
            return True
        return False
def admin(request):
    return redirect('admin')
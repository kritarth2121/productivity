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
import datetime
from users import views as user_views

from .models import Post,Views,Team,TeamMember
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

def admi(request):
    if request.user.is_superuser:
        context = {
                'team':Team.objects.filter(owner=request.user),

            }
        print(context)
        
        return render(request, 'blog/team.html', context)
    else:
        return redirect('blog-home')
def teammembers(request,name):
    if request.user.is_superuser:
        context = {
                'team':TeamMember.objects.filter(team__name=name),

            }
        
        print(context)
        return render(request, 'blog/teammembers.html', context)

class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

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
    def get_queryset(self):
        user = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        print(user.id)
        return Post.objects.filter(id=user.id)


class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    fields = ['assigned_employee','work_today', 'work_done']
    template_name='blog/post_detail.html'
    def form_valid(self, form):
            return super().form_valid(form)
    def test_func(self):
        #post = self.get_object()
        if self.request.user.is_superuser:
            return True
        return False
@login_required
def create(request):
    print(datetime.datetime.now().hour)
    if (Post.objects.filter(date_posted__day=datetime.datetime.now().day , date_posted__month=datetime.datetime.now().month , date_posted__year=datetime.datetime.now().year).count()==0 ) or (Post.objects.get(date_posted__day=datetime.datetime.now().day,assigned_employee=request.user).work_done==None and (int(datetime.datetime.now().hour)>=18 or int(datetime.datetime.now().hour)<=3)):

        if int(datetime.datetime.now().hour)>=6 and int(datetime.datetime.now().hour)<18:
            if request.method == 'POST':
                today=request.POST['today']
                ins=Post.objects.create(work_today=today,assigned_employee=request.user,date_posted=datetime.datetime.now())
                ins.save()
                return render(request, 'blog/home.html')
            else:
                return render(request, "blog/post_form.html" )
        elif (int(datetime.datetime.now().hour)>=18 and int(datetime.datetime.now().hour)<=24) or (int(datetime.datetime.now().hour)>0 and int(datetime.datetime.now().hour<=3)):
            if request.method == 'POST':
                today=request.POST['today']
                if Post.objects.filter(date_posted__day=datetime.datetime.now().day,assigned_employee=request.user).count()==1:
                    insta=Post.objects.get(date_posted__day=datetime.datetime.now().day,assigned_employee=request.user)
                    insta.work_done=today
                    insta.save()
                    print("created")
                    
                    return redirect('blog-home')
                elif Post.objects.filter(date_posted__day=(datetime.datetime.now().day-1)).count()==1:
                    insta=Post.objects.get(date_posted__day=datetime.datetime.now().day)
                    insta.work_done=today
                    insta.save()
                    return redirect('blog-home')


            else:
                if Post.objects.filter(date_posted__day=datetime.datetime.now().day,assigned_employee=request.user) or Post.objects.filter(date_posted__day=(datetime.datetime.now().day-1),assigned_employee=request.user):
                    insta=Post.objects.get(date_posted__day=datetime.datetime.now().day,assigned_employee=request.user)
                    context={
                        'post':insta.work_today
                    }
                    return render(request, "blog/post_form1.html" ,context)
                else:
                    return render(request, "blog/notdone.html" )
        else:
            return render(request, "blog/return.html" )
    else:
        return render(request, "blog/once.html" )
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
                    return render(request, 'blog/home.html')
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
                        
                        return redirect('blog-home')
                else:
                    insta=Post.objects.get(id=pk)
                    context={
                        'post':insta.work_today
                    }
                    return render(request, "blog/post_form1.html" ,context)
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
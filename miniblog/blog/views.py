from django.shortcuts import render, HttpResponseRedirect
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as authlogin, logout
from .models import *
from django.contrib.auth.models import Group
# Create your views here.


#HOME PAGE
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})


#ABOUT PAGE
def about(request):
    return render(request, 'about.html')


#CONTACT PAGE
def contact(request):
    return render(request, 'contact.html')


#DESHBOARD PAGE
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        fullname = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'dashboard.html', {'posts': posts,'full_name':fullname,'groups':gps})
    else:
        HttpResponseRedirect('/login/')


#LOGOUT

def user_logout(request):
        logout(request)
        return HttpResponseRedirect('/')


#Signup
def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations !! You have become an Authot.')
            user = form.save()
            form = SignUpForm()
            group = Group.objects.get(name='author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


    #Login
def loginfun(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upss = fm.cleaned_data['password']
                users = authenticate(username=uname, password=upss)
                if users is not None:
                    authlogin(request, users)
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = LoginForm()
        return render(request, 'login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dashboard/')


#add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


 #update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


        #delete post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

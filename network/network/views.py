from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json 
from django.core.paginator import Paginator
from django.template.defaulttags import register

from .models import User,Post,Like, Follow


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@login_required(login_url="login")
def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    paginator = Paginator(posts,10)
    pageNumber = request.GET.get('page')
    postsPage = paginator.get_page(pageNumber)
    query = Like.objects.filter(user=request.user)
    postsYouLiked = []
    likes = {}
    for post in query:
        postsYouLiked.append(post.post)
    
    for p in posts:
        like = len(Like.objects.filter(post=p))
        likes[p.id] = like
    return render(request, "network/index.html",{
        "posts": posts,
        "postsPage": postsPage,
        "postsYouLiked": postsYouLiked,
        "likes": likes
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request):
    if request.method == "POST":
        text = request.POST["text"]
        post = Post(poster=request.user,text=text)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"network/newPost.html")



@login_required(login_url='login')
def profile(request,userId):
    if request.method == "GET":
        user = User.objects.get(pk=userId)
        userPosts = Post.objects.filter(poster=user).order_by("id").reverse()
        paginator = Paginator(userPosts,10)
        pageNumber = request.GET.get('page')
        postsPage = paginator.get_page(pageNumber)
        followers = Follow.objects.filter(userFollowed=user)
        following = Follow.objects.filter(user=user)
        likes = {}
        for p in userPosts:
            like = len(Like.objects.filter(post=p))
            likes[p.id] = like
        try:
            if Follow.objects.get(user=request.user,userFollowed=user):
                isFollowing =  True
        except:
            isFollowing = False
        return render(request, "network/profile.html",{
            "posts": userPosts,
            "postsPage": postsPage,
            "username": user.username,
            "following": len(following),
            "followers": len(followers),
            "profile": user,
            "isFollowing": isFollowing,
            "likes": likes
        })

def follow(request):
    if request.method == "POST":
        usernameToFollow = request.POST["userToFollow"]
        userToFollow = User.objects.get(username=usernameToFollow)
        f = Follow(user=request.user,userFollowed=userToFollow)
        f.save()
        return redirect("profile",userId=userToFollow.id)

def unfollow(request):
    if request.method == "POST":
        usernameToUnfollow = request.POST["userToUnfollow"]
        userToUnfollow = User.objects.get(username=usernameToUnfollow)
        f = Follow.objects.get(user=request.user,userFollowed=userToUnfollow)
        f.delete()
        return redirect("profile",userId=userToUnfollow.id)


def following(request):
    if request.method == "GET":
        allPosts = Post.objects.all().order_by("id").reverse()
        following = Follow.objects.filter(user=request.user)
        posts = []
        for post in allPosts:
            for person in following:
                if post.poster == person.userFollowed:
                    posts.append(post)
        
        query = Like.objects.filter(user=request.user)
        postsYouLiked = []
        for post in query:
            postsYouLiked.append(post.post)
        paginator = Paginator(posts,10)
        pageNumber = request.GET.get('page')
        postsPage = paginator.get_page(pageNumber)
        likes = {}
        for p in posts:
            like = len(Like.objects.filter(post=p))
            likes[p.id] = like
        
        return render(request, "network/following.html", {
            "posts": postsPage,
            "likes": likes,
            "postsYouLiked": postsYouLiked
        })

def editPost(request,postId):
    if request.method == "POST":
        post = Post.objects.get(pk=postId)
        newContent = json.loads(request.body)
        post.text = newContent["content"]
        post.save()
        return JsonResponse({
            "message": "Successfull fetch",
            "newContent": newContent["content"]
        })

def increaseLike(request,postId):
    if request.method == "POST":
        post = Post.objects.get(pk=postId)
        l = Like(post=post,user=request.user)
        l.save()
        numberOfLikes = len(Like.objects.filter(post=post))
        return JsonResponse({
            "message": "Like increased succesfully",
            "numberOfLikes": numberOfLikes
        })

def decreaseLike(request,postId):
    if request.method == "POST":
        post = Post.objects.get(pk=postId)
        l = Like.objects.get(post=post,user=request.user)
        l.delete()
        numberOfLikes = len(Like.objects.filter(post=post))
        return JsonResponse({
            "message": "Like decreased successfully", 
            "numberOfLikes": numberOfLikes
        })


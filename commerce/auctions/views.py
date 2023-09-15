from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponse
from django.contrib import messages


from .models import User,Category,AuctionListing,WatchList,Bid,Comment,Notifications


class NewForm(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="Description",widget=forms.TextInput(attrs={'class': 'form-control'}))
    startingBid = forms.FloatField(label="Starting bid",widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(required=False,queryset=Category.objects.all(), label="Category", widget=forms.Select(attrs={'class': 'form-control'}))
    url = forms.CharField(label="Image url", required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    isActive = forms.BooleanField(label="Active?",initial=True,widget=forms.CheckboxInput(attrs={'class': 'form-check'}))




def index(request):
    return render(request, "auctions/index.html", {
        "activeListings": AuctionListing.objects.filter(isActive = True),
        "categories": Category.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startingBid = form.cleaned_data["startingBid"]
            category = form.cleaned_data["category"]
            url = form.cleaned_data["url"]
            isActive = form.cleaned_data["isActive"]



            newAuctionListing = AuctionListing(title=title,description=description,startingBid=startingBid,actualBid=startingBid,url=url,owner=request.user,category=category,isActive=isActive)
            newAuctionListing.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form = NewForm()
            return render(request,"auctions/create.html", {
                "message": "Invalid Form",
                "form" : form
            })
    else:
        form = NewForm()
        return render(request,"auctions/create.html", {
            "form": form
        })


@login_required(login_url='login')
def listing(request,id):
    auction = AuctionListing.objects.get(pk=id)
    presence = WatchList.objects.filter(user=request.user,list=auction)
    totalBids = len(Bid.objects.all())
    comments = Comment.objects.filter(list=auction)
    isPresent = None
    if presence:
        isPresent = True
    else:
        isPresent = False
    if request.method == "GET":
        return render(request,"auctions/listing.html",{
            "auction": auction,
            "presence": isPresent,
            "bids": totalBids,
            "comments": comments
        })

def clickCategory(request,type):
    c = Category.objects.get(type=type)
    au = AuctionListing.objects.filter(category=c)
    return render(request,"auctions/index.html", {
        "activeListings": au,
        "categories": Category.objects.all()
    })

def listCategory(request):
    if request.method == "POST":
        CategoryForm = request.POST["category"]
        CategoryObject = Category.objects.get(type=CategoryForm)
        AuctionListingObjects = AuctionListing.objects.filter(category=CategoryObject,isActive=True)
        return render(request,"auctions/index.html", {
            "activeListings": AuctionListingObjects,
            "categories": Category.objects.all()
        })

def removeWatchList(request,id):
    auction = AuctionListing.objects.get(pk=id)
    wl = WatchList.objects.get(user=request.user,list=auction)
    wl.delete()
    if request.method == "POST":
        return render(request,"auctions/listing.html",{
            "auction": auction,
            "presence": False
        })

def addWatchList(request,id):
    auction = AuctionListing.objects.get(pk=id)
    wl = WatchList(user=request.user,list=auction)
    wl.save()
    if request.method == "POST":
        return render(request,"auctions/listing.html",{
            "auction": auction,
            "presence": True
        })

def closeList(request,id):
    al = AuctionListing.objects.get(pk=id)
    al.isActive = False
    al.save()
    #Add a notification for the winner user
    n = Notifications(user=al.lastOferrer,message= f"You have won the bid for the {al.title} with {al.actualBid}€")
    n.save()
    return render(request,"auctions/index.html", {
        "activeListings": AuctionListing.objects.filter(isActive = True),
        "categories": Category.objects.all()
    })

def placeBid(request,id):
    al = AuctionListing.objects.get(pk=id)
    presence = WatchList.objects.filter(user=request.user,list=al)
    isPresent = False
    message=False
    if presence:
        isPresent = True
    if request.method == "POST" and request.user != al.owner:
        newBid = request.POST["bidNumber"]
        if float(newBid) > float(al.actualBid):
            al.actualBid = newBid
            al.lastOferrer = request.user
            al.save()
            bid = Bid(oferrer=request.user,watchlist=al)
            bid.save()
        else:
            message = "The new bid has to be greater than the previous one"
    return render(request,"auctions/listing.html", {
            "auction": al,
            "presence": isPresent,
            "bids":  len(Bid.objects.filter(watchlist=al)),
            "message": message
    })

def displayWatchList(request):
    if request.method == "GET":
        query = WatchList.objects.filter(user=request.user)
        watchlist = []
        for u in query:
            watchlist.append(u.list)
        print(len(watchlist))
        return render(request,"auctions/watchlist.html", {
            "watchlist" : watchlist
        }) 

def postComments(request,id):
    l = AuctionListing.objects.get(pk=id)
    if request.method == "POST":
        body = request.POST["comment"]
        c = Comment(poster=request.user,list=l,body=body)
        c.save()
        return render(request,"auctions/listing.html", {
            "auction": l,
            "comments": Comment.objects.filter(list=l)
        })

def notifications(request):
    return render(request,"auctions/notifications.html", {
        "notifications": Notifications.objects.filter(user=request.user)
    })



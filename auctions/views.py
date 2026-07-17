from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import*

from .models import User


def index(request):
    return render(request, "auctions/index.html",{
        "Listings" : Listing.objects.all()
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
    

def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create.html",{
            "Categories" : Category.objects.all()
        })
    elif request.method == "POST":
        title = request.POST.get("title")
        description= request.POST.get("description")
        image_URL = request.POST.get("image_URL")
        category_id= Category.objects.get(id = request.POST.get("Category"))
        owner = request.user
        starting_bid = request.POST.get("starting_bid")

        Listing.objects.create(
            title=title,
            description=description,
            owner=owner,
            image_url = image_URL,
            starting_bid = starting_bid,
            category_id = category_id
        )
        return redirect("index")

def listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    watchlisted = Watchlist.objects.filter(owner= request.user, listing = listing).exists()
    if request.method == "GET":
        if request.user.is_authenticated:  
            return render(request, "auctions/listing.html",{
            "comments" : Comments.objects.all(),
            "listing" : listing,
            "watchlisted" : watchlisted
        } )
    elif request.method == "POST":
        comment = request.POST.get("comment")
        if "placed_bid" in request.POST : 
            placed_bid = request.POST.get("placed_bid")
            Bids.objects.create(
                listing = listing,
                bidder = request.user,
                amount = placed_bid                             
            )
        elif "comment" in request.POST:
            Comments.objects.create(
                listing = listing,
                owner = request.user,
                content = comment,
        )
        elif "toggle_watchlist" in request.POST:
            if watchlisted :
                Watchlist.objects.filter(owner= request.user, listing= listing).delete()
            else:
                Watchlist.objects.create(owner = request.user, listing=listing)
        return redirect("listing", listing_id = listing_id)
    

def watchlist(request):
    watch_list = [entry.listing for entry in Watchlist.objects.filter(owner=request.user)]
    return render(request, "auctions/watchlist.html",{
        "watch_list" : watch_list 
    })
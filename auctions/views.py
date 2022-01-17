from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Category, Bid
from .forms import BidForm, CommentForm, NewListingForm


def index(request):
    active_listings = Listing.objects.filter(
        ended_manually=False, end_time__gte=datetime.now()
    )
    return render(request, "auctions/index.html", {"listings": active_listings})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id: int, message: str = None):
    listing = Listing.objects.get(pk=listing_id)
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "message": message,
            "bid_form": BidForm(),
            "comment_form": CommentForm(),
        },
    )


@login_required(login_url="auctions/login.html")
def bid_listing(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            user_bid = form.cleaned_data["bid"]
            if listing.bids.all():
                highest_bid = max([bid.bid for bid in listing.bids.all()])
            else:
                highest_bid = listing.starting_bid
            if user_bid > highest_bid:
                Bid(bid=user_bid, bidder=request.user, listing=listing).save()
                return HttpResponseRedirect(
                    reverse("listing", kwargs={"listing_id": listing_id})
                )
            else:
                return HttpResponseRedirect(
                    reverse(
                        "listing",
                        kwargs={
                            "listing_id": listing_id,
                            "message": "Your bid wasn't big enough!",
                        },
                    )
                )


@login_required(login_url="auctions/login.html")
def comment_listing(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            Comment(listing=listing, creator=request.user, comment=comment).save()
            return HttpResponseRedirect(
                reverse("listing", kwargs={"listing_id": listing_id})
            )
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


@login_required(login_url="auctions/login.html")
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["starting_bid"]
            try:
                img = form.cleaned_data["img"]
            except:
                img = None
            try:
                category = Category.objects.filter(name=form.cleaned_data["category"])
                category.save()
            except:
                category = None
            duration = int(form.cleaned_data["duration"]) or None
            listing = Listing(
                title=title,
                description=description,
                starting_bid=start_bid,
                img=img,
                category=category,
                duration=duration,
                creator=request.user,
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {"form": NewListingForm()})


def close_listing(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    if request.user == listing.creator:
        listing.ended_manually = True
        listing.save()

    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


def watch_listing(request, listing_id: int):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = request.user.watchlist
    if listing in watchlist.all():
        watchlist.remove(listing)
    else:
        watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))


def category(request, category_name: str):
    cat = Category.objects.get(name=category_name)
    auctions = Listing.objects.filter(
        category=cat, ended_manually=False, end_time__gte=datetime.now()
    )
    return render(
        request,
        "auctions/index.html",
        {"listings": auctions, "category_name": category_name},
    )


def categories_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/index.html", {"listings": listings})

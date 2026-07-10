from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="listings", blank=True)
    starting_bid = models.DecimalField(max_digits = 10, decimal_places = 2)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} {self.is_active}"


class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    placed_at = models.DateTimeField(auto_now_add = True)
    amount = models.DecimalField(decimal_places=2, max_digits = 10)
    def __str__(self):
        return f"{self.listing} {self.amount}"
    
class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    owner =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return f"{self.listing} {self.posted_at}"

class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="Watchlisted_by")
    def __str__(self):
        return f"{self.owner} {self.listing}"
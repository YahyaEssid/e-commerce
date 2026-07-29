from django.contrib import admin

from auctions.models import Listing, Category, Bids, Comments, Watchlist
# Register your models here.

admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)
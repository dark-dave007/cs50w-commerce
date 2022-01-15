from django.contrib import admin

from auctions.views import register
from .models import Category, User, Listing, Comment, Bid

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "category", "creator")


class CategoryAdmin(admin.ModelAdmin):
    ordering = ["name"]


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid)

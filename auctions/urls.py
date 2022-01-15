from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories_list, name="categories"),
    path("categories/<str:category_name>", views.category, name="category"),
    path("listings/create_listing", views.create_listing, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/bid", views.bid_listing, name="bid_listing"),
    path("listings/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("listings/<int:listing_id>/comment", views.comment_listing, name="comment"),
    path("listings/<int:listing_id>/watch", views.watch_listing, name="watch_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
]

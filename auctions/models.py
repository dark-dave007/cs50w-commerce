from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        # order alphabetically
        ordering = ("name",)

    def __str__(self) -> str:
        return str(self.name)


class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=512)
    starting_bid = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0.01)]
    )
    img = models.CharField(blank=True, null=True, max_length=256)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="listings",
    )

    creator: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    DURATIONS = (
        (1, "One Day"),
        (3, "Three Days"),
        (7, "One Week"),
        (14, "Two Weeks"),
        (28, "Four Weeks"),
    )
    duration = models.IntegerField(choices=DURATIONS, default=7)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    ended_manually = models.BooleanField(default=False)

    def __str__(self):
        return f"Listing #{self.id}: {self.creator.username} | {self.title}"

    def save(self, *args, **kwargs):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(days=self.duration)
        super().save(*args, **kwargs)  # call existing save() method

    def ended(self):
        if self.ended_manually or self.end_time < timezone.now():
            return True
        else:
            return False


class Bid(models.Model):
    bid = models.DecimalField(
        decimal_places=2, max_digits=12, validators=[MinValueValidator(0.01)]
    )
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    class Meta:
        ordering = ("-bid",)

    def __str__(self) -> str:
        return f"Bid #{self.id}: {self.bidder} on {self.listing} for {self.bid}"


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1024)
    listing = models.ForeignKey(
        Listing,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta:
        ordering = ("-comment",)

    def __str__(self) -> str:
        return f"Comment #{self.id}: {self.creator} on {self.listing}"

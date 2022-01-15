from django import forms
from .models import Category, Listing


class NewListingForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": True,
                "placeholder": "Title:",
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Description:"}
        )
    )
    starting_bid = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "25"})
    )
    duration = forms.ChoiceField(
        required=False,
        choices=Listing.DURATIONS,
        widget=forms.Select(attrs={"class": "form-control", "value": "7"}),
    )
    img = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "www.example.com/joe.png"}
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class BidForm(forms.Form):
    bid = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": "1",
                "placeholder": "Comment:",
                "type": "submit",
            }
        )
    )

from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm

from vinyl.models import Album, Genre, User, Collection


class AlbumForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Album
        fields = ["title", "artist", "genres", "year", "cover"]

    def clean_year(self):
        year = self.cleaned_data.get("year")
        current_year = date.today().year
        if year is not None and not (1900 <= year <= current_year):
            raise forms.ValidationError(
                f"Year must be between 1900 and {current_year}."
            )
        return year


class CollectionerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "country",
        )


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["status", "rating", "condition"]


class AlbumSearchForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title",
            }
        )
    )

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from vinyl.forms import AlbumForm, CollectionerCreationForm, CollectionForm
from vinyl.models import Genre, Artist, Album, User, Collection


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_users = User.objects.count()
    num_albums = Album.objects.count()
    num_artists = Artist.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_users": num_users,
        "num_albums": num_albums,
        "num_artists": num_artists,
        "num_visits": num_visits + 1,
    }

    return render(request, "vinyl/index.html", context=context)


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name = "vinyl/genre_list.html"
    context_object_name = "genres"
    paginate_by = 15


class GenreCreateView(LoginRequiredMixin, generic.CreateView):
    model = Genre
    fields = "__all__"
    template_name = "vinyl/genre_form.html"
    success_url = reverse_lazy("vinyl:genre-list")


class GenreUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Genre
    fields = "__all__"
    template_name = "vinyl/genre_form.html"
    success_url = reverse_lazy("vinyl:genre-list")


class GenreDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Genre
    template_name = "vinyl/genre_confirm_delete.html"
    success_url = reverse_lazy("vinyl:genre-list")




class ArtistListView(LoginRequiredMixin, generic.ListView):
    model = Artist
    template_name = "vinyl/artist_list.html"
    context_object_name = "artists"
    paginate_by = 15


class ArtistCreateView(LoginRequiredMixin, generic.CreateView):
    model = Artist
    fields = "__all__"
    template_name = "vinyl/artist_form.html"
    success_url = reverse_lazy("vinyl:artist-list")


class ArtistUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Artist
    fields = "__all__"
    template_name = "vinyl/artist_form.html"
    success_url = reverse_lazy("vinyl:artist-list")


class ArtistDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Artist
    template_name = "vinyl/artist_confirm_delete.html"
    success_url = reverse_lazy("vinyl:artist-list")

class ArtistDetailView(LoginRequiredMixin, generic.DetailView):
    model = Artist
    template_name = "vinyl/artist_detail.html"
    context_object_name = "artist"




class AlbumListView(LoginRequiredMixin, generic.ListView):
    model = Album
    template_name = "vinyl/album_list.html"
    context_object_name = "albums"
    paginate_by = 18
    queryset = Album.objects.select_related("artist")

    def get_queryset(self):
        queryset = Album.objects.select_related("artist")
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset


class AlbumCreateView(LoginRequiredMixin, generic.CreateView):
    model = Album
    form_class = AlbumForm
    template_name = "vinyl/album_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = "vinyl/album_form.html"


class AlbumDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Album
    template_name = "vinyl/album_confirm_delete.html"
    success_url = reverse_lazy("vinyl:album-list")


class AlbumDetailView(LoginRequiredMixin, generic.DetailView):
    model = Album
    template_name = "vinyl/album_detail.html"
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_collection = None

        if self.request.user.is_authenticated:
            user_collection = Collection.objects.filter(
                user=self.request.user,
                album=self.object
            ).first()

        context["user_collection"] = user_collection
        return context


class AlbumByYearView(LoginRequiredMixin, generic.ListView):
    model = Album
    template_name = "vinyl/album_list.html"
    context_object_name = "albums"

    def get_queryset(self):
        return (
            Album.objects
            .filter(year=self.kwargs["year"])
            .select_related("artist")
            .prefetch_related("genres")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = self.kwargs["year"]
        return context




class UsersCreateView(generic.CreateView):
    model = User
    form_class = CollectionerCreationForm
    success_url = reverse_lazy("login")




class CollectionAddView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        album = Album.objects.get(pk=pk)

        Collection.objects.get_or_create(
            user=request.user,
            album=album,
            defaults={"status": "owned"},
        )

        return redirect(album.get_absolute_url())


class CollectionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Collection
    form_class = CollectionForm
    template_name = "vinyl/collection_form.html"
    success_url = reverse_lazy("vinyl:my-collection")

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)


class CollectionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Collection
    template_name = "vinyl/collection_confirm_delete.html"
    success_url = reverse_lazy("vinyl:my-collection")

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)




class MyCollectionView(LoginRequiredMixin, generic.ListView):
    model = Collection
    template_name = "vinyl/my_collection.html"
    context_object_name = "items"

    def get_queryset(self):
        return (
            Collection.objects
            .filter(user=self.request.user)
            .select_related("album", "album__artist")
        )
